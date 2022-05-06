from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc import WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

import configparser

class WP:

    def __init__(self, site, user, passwd):
        self.wp = Client(site, user, passwd)

    def PostNew(self, title, html_body, post_tag, category):
        post = WordPressPost()
        post.title = title
        post.content = html_body
        post.post_status = 'publish' #文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布
        
        post.terms_names = {
            'post_tag': post_tag, #文章所属标签，没有则自动创建
            'category': category #文章所属分类，没有则自动创建
        }
        
        post.id = self.wp.call(posts.NewPost(post))

        return post.id

    def testPostNew(self):
        title =  'test' 
        html_body = '<div> this is test </div>'
        post_tag = ['xml', 'python']
        category = ['硬核知识']
        self.PostNew( title, html_body, post_tag,  category )


if __name__ == '__main__':

    cfg = './config.ini'
    # 创建配置文件对象
    con = configparser.RawConfigParser()
    # 读取文件
    con.read(cfg, encoding='utf-8')

    cdict = dict( con.items('wordpress') )

    wp = WP( cdict['url'], cdict['username'], cdict['password'] )

    wp.testPostNew()
    