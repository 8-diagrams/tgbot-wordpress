import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


import configparser

cfg = './config.ini'
# 创建配置文件对象
con = configparser.ConfigParser()
# 读取文件
con.read(cfg, encoding='utf-8')

class UserData:
    def __init__(self):
        self._data = {}
    
    def get(self, key):
        if not self._data.get(key):
            self._data[key] = {}
        return self._data[key]

    def set(self, key, value):
        self._data[key] = value

StatusMap = UserData()

def getSendKey():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='McFlurry', callback_data='McFlurry'),InlineKeyboardButton(text='nima', callback_data='cow')],
                   [InlineKeyboardButton(text='Nugget', callback_data='Nugget')],
                   [InlineKeyboardButton(text='Coke', callback_data='Coke')],
                   [InlineKeyboardButton(text='Coke', url='http://www.baidu.com')],
               ])
    return      keyboard    

def genKeyBoard(text):
    #
    keyword = 'all'
    desca = '请选择'
    inline_keyboard = []
    line_of_button = []
    lines = text.split("\n")
    new_line = []
    for line in lines:
        line = line.strip()
        if line.find("=>") == -1 and line.find("[换行]") == -1 and line.find("[关键字]") :
            continue
        print (line)
        if line == "[换行]":
            line_of_button.append( new_line )
            new_line = []
        else:
            key , value = line.split("=>")
            key = key.strip()
            value = value.strip()
            if key == '[关键字]':
                keyword = value
            elif key == '[描述]':
                desca = value
            else:
                new_line.append( (key , value) )

    if new_line :
        line_of_button.append( new_line )

    for buttons in line_of_button:
        lob = []
        for button in buttons:
            if button[1].lower().find('http') == 0:
                print ("URL ", button )
                lob.append( InlineKeyboardButton( text = button[0], url = button[1] ) )
            else:
                print ("text ", button )
                lob.append( InlineKeyboardButton( text = button[0], callback_data = button[1] ) )
        inline_keyboard.append( lob )

    return keyword, desca, InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
       

def Setting(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    botdict = dict( con.items('bot') ) 
    admin_line = botdict["admin"]
    print  ( "setting admin line " + str(admin_line) )
    admins = [ x.strip() for x in  admin_line.split(',') ]
    for item in admins:
        print  ( "setting admin for " + str(item) )
        admin_id = int( item )
        bot.sendMessage(admin_id, """输入你的按钮设置:，回复如下字样\n
[关键字] => go
[描述] => 你需要用什么搜索：
谷歌 => 访问google.com \n
搜狗 => 访问sogou.com \n
[换行]
去百度搜索 => http://www.baidu.com \n
        """)
        
        StatusMap.get( admin_id )["status"] = "wait_bot_setting"
        StatusMap.get( admin_id )["chanel_id"] = chat_id
    
def  MakeSetting( msg ):
    print ( msg['text'] )
    keyword, desca, setting = genKeyBoard( msg['text'] )
    content_type, chat_type, chat_id = telepot.glance(msg)
    chanel_id = StatusMap.get( chat_id ).get("chanel_id")
    import os
    rpath = "./"+ str(chanel_id) + "/"
    if not os.path.exists(rpath):
        os.mkdir( rpath )
    fpath = rpath  + keyword + ".txt"
    f = open(fpath, "w")
    f.write( msg['text'] )
    f.close()
    StatusMap.get( chat_id )["status"] = ''


def ParseSetting( text) :
    pass

def checkPostSetting( msg ):

    content_type, chat_type, chat_id = telepot.glance(msg)
    messageid = msg['message_id']
    keyword = msg['text'].strip()
    #StatusMap.get(chat_id).get("")
    keyword = keyword.split(" ")[0]
    print ( "关键词：" + keyword )
    try:

        import os
        rpath = "./"+ str(chat_id) + "/"
        fpath = rpath  + keyword + ".txt"
        try:
            print ("FIND 1 " + fpath )
            f = open( fpath , "r")
        except Exception as E2:
            fpath = rpath  + 'all' + ".txt"
            print ("FIND 1 " + fpath )
            f = open( fpath , "r")
        
        text = f.read()
        f.close()
        print (" READ TEXT " + text )
        k, desca, keyboard = genKeyBoard(text)
        desca = ""
        #bot.sendMessage( chat_id, text=desca, reply_markup = keyboard)
        print ( "MSG  MARKUP " + str((chat_id, messageid)) )
        bot.editMessageReplyMarkup( msg_identifier=(chat_id, messageid), reply_markup = keyboard)
    except Exception as e:
        pass
        import traceback
        traceback.print_exc()

def on_callback_query(msg):
    print ( str(msg ) )

def procCallback(msg):
    data = msg["data"]
    chanel_id = msg["message"]["sender_chat"]["id"]
    bot.sendMessage( chanel_id, data )

def handle(msg):
    try :
        print ( "MSG:: " , str(msg) )
        if 'chat_instance' in msg.keys() and 'message' in msg.keys() and 'data' in  msg.keys():
            return procCallback( msg )
        content_type, chat_type, chat_id = telepot.glance(msg)

        print(content_type, chat_type, chat_id)
        botdict = dict( con.items('bot') ) 
        admin_line = botdict["admin"]
        admins = [ int( x.strip() ) for x in  admin_line.split(',') ]

        if chat_id in admins :
            if StatusMap.get( chat_id ).get("status") == "wait_bot_setting" :
                return MakeSetting( msg )


        if chat_type == 'channel_post':
            if msg['text'] == '/set':
                return Setting(msg)

            return checkPostSetting(msg)


    except Exception as e:
        import traceback
        traceback.print_exc()
        print ( str(e) )
    

botdict = dict( con.items('bot') ) 
TOKEN = botdict["key"]

bot = telepot.Bot(TOKEN)

#MessageLoop(bot, { 'chat': handle,
#                  'callback_query': on_callback_query} ).run_as_thread()
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

