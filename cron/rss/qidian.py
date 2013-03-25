# coding=utf-8
""" 对rss 进行分析"""

var = """

<?xml version="1.0" encoding="utf-8"?>
<rss version="2.0">
<channel>
<title>起点中文网小说榜单</title>
<link>http://top.qidian.com/</link>
<description>最新热门小说排行榜是用户推举的小说排行榜,包含各类小说排行榜,小说排行榜上都是受用户欢迎的小说作品</description>
<language>zh-cn</language>
<pubDate>Sat, 23 Mar 2013 19:07:36 GMT</pubDate>
<lastBuildDate>Sun, 19 May 2002 15:21:36 GMT</lastBuildDate>
<managingEditor>xxxxx@snda.com</managingEditor>
<webMaster>xxxxx@snda.com</webMaster>
<ttl>180</ttl>
<copyright>Copyright (C) 2002-2010 www.qidian.com All Rights Reserved</copyright>
<generator>RSS Service By Qidian</generator>
<item>
   <category >都市</category>
   <link>http://www.qidian.com/Book/2568342.aspx</link>
   <title>1. 《都市大巫》 起点中文网_强力推荐</title>
   <author>白马神</author>
   <description><![CDATA[1. 《都市大巫》 起点中文网_强力推荐
   作者:白马神<br/>原书链接:<a target='_blank' href='http://www.qidian.com/Book/2568342.aspx'>点击立即阅读</a>]]></description>
   <pubDate>Sat, 23 Mar 2013 00:00:01 GMT</pubDate>
   <guid isPermaLink="true">http://www.qidian.com/Book/2568342.aspx</guid>
   <comment>http://forum.qidian.com/bookforumnew.aspx?bookid=2568342</comment>
</item>
</channel>
</rss>

"""


import urllib
import feedparser

class RssContent:
    """ 根据url获得页面的内容用于数据分析 """
    def __init__(self,url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()
    def getData(self):
        return self.htmlSource



if __name__ == "__main__":
    # myContent = RssContent("http://www.qidian.com/rss.aspx")
    # print myContent.getData()
    d = feedparser.parse("http://www.qidian.com/rss.aspx")
    print d.channel.title
    print d.feed.link
    print d.channel.description
    print len(d['entries'])
    print d['entries'][0]['title']
    print d.entries[0].title
    print d['items'][0].title
    print d.entries[0].link






