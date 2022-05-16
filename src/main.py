import time
import telepot
from telepot.loop import MessageLoop

import configparser

cfg = './config.ini'
# 创建配置文件对象
con = configparser.ConfigParser()
# 读取文件
con.read(cfg, encoding='utf-8')

StatusMap = {}

def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    print(content_type, chat_type, chat_id)
    if not StatusMap.get(chat_id ) :
        StatusMap[ chat_id ] = {}
    
    if StatusMap[ chat_id ].get("status") == "waiting" or len( msg['text']  ) > 100 :
        post = msg['text'] 
        if len(post) < 30:
            bot.sendMessage(chat_id , "字数条少 "  )
            return 

        bot.sendMessage(chat_id , "向WP提交 "  )

        ret = postNew( post )

        bot.sendMessage(chat_id , "发送结果 " + str(ret) )
        StatusMap[ chat_id ]["status"] = ''

    if msg['text'] == '/new':
        bot.sendMessage(chat_id, '发送文章内容:')
        StatusMap[ chat_id ]["status"] = "waiting"
    elif msg['text'] == '/how':
        bot.sendMessage(chat_id, '你发送了how')
    
def parsePost(post):

    try:
        title = []
        idx = 0 
        for c in post :
            if c == '\n':
                break;
            else:
                title.append( c )
                idx += 1
                if idx > 64:
                    break

        title = "".join( title)

        import re
        c = re.compile(r"\#[^ \#]{1,20}")

        tags = c.findall( post)

        tags = [ x[1:] for x in tags ]

        return title, tags, post 
    except Exception as e:
        return post[:64], [], post


def postNew(post):
    cfg = './config.ini'
    # 创建配置文件对象
    con = configparser.RawConfigParser()
    # 读取文件
    con.read(cfg, encoding='utf-8')
    cdict = dict( con.items('wordpress') )
    
    title, tags, post = parsePost(post)
    import XmlWp
    wp = XmlWp.WP( cdict['url'], cdict['username'], cdict['password'] )
    category = ['信息速递']
    ret = wp.PostNew(title, post, tags, category)
    return ret  

botdict = dict( con.items('bot') ) 
TOKEN = botdict["key"]

bot = telepot.Bot(TOKEN)

MessageLoop(bot, handle).run_as_thread()

print ('BOT ...')

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
import sys
sys.stdout = Unbuffered(sys.stdout)


# Keep the program running.
while 1:
    time.sleep(10)

