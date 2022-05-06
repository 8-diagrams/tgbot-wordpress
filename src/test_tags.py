from jieba import analyse
textrank = analyse.textrank  #引入jieba中的TextRank
text="""之前在windows下使用onenote写作的时候,是使用onenote自带的功能直接将写好的文章发送到博客中去的,现在到了mac下,此功能的快捷性不再.无奈只好定制自己的一键发送到博客.
想了想,apple script自己现在掌握还不好,定制自己的work flow也还一时不知如何入手,倒是想到之前使用onenote的时候,需要到博客后台管理界面启动个接口,随便查了下,查到这个接口是所谓的xml-rpc接口,也就是说通过xml来对wordpress进行远程调用,然后发布文章的接口.
既然明白了原理,接下来的事情就简单了,我之前有种中二病,有什么问题老想自己从编译器开始全部重新解决一下,后来在搜狗的时候,leader李东阳告诉自己一个深刻的道理,不要重复造轮子.这才慢慢地把这个贱毛病给扭转过来,算是上了道.
我一直认为自己是个科研工作者,虽然做的码农活的,不过时常看看论文,推个公式,聊以自谓下:哥还没有完全脱离理论界.
做事先求解决.再说进一步的问题.
首先在git里找wordpress,找到了一个包,但是几乎一直没有维护,将其拿过来看了看,只有一个主文件,定义了一个类,而且使用的主要是xmlrpclib这么一个库.
之后又转到了google的站长工具那里瞅了两眼,然后终于找到了正确的keywords.
python xmlrpclib wordpress
ok,发现了一个封闭了xmlrpclib的一个python包,针对wordpress.很好.立即pip一下,使用之.
在readthedocs中,有这包的使用文档.python-wordpress-xmlrpc.readthedocs.org/en/latest/o…
简单地搬运一下quickstart.

作者：步入云端
链接：https://juejin.cn/post/6893683665902469134
来源：稀土掘金
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。"""
keywords = textrank(text)
print(keywords)


t2="""技术 #博客 《老农的博客 (https://303248153.github.io/)》

博客内容为三个系列：写给程序员的机器学习入门 、Golang源码探索、CoreCLR源码探索。最详细的是 #机器学习 入门系列文章。

“这个系列的阅读目标是程序员，主要是那些人到中年，天天只做增删查改，并且开始掉头发的程序员们，他们很多都抱怨其他高级的教程看不懂。所以这个系列会把容易理解放在首位，看完可能只能做个调参狗，但如主席所说的，不管黑狗白狗，能解决问题的就是好狗。希望这个系列可以让你踏入机器学习的大门，并且可以利用机器学习解决业务上的问题。”"""

title = []
idx = 0 
for c in t2 :
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

tags = c.findall(t2)

tags = [ x[1:] for x in tags ]

print ( tags )



print (title)