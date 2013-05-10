# coding=utf-8

import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")

import random
import re
import urllib
from sgmllib import SGMLParser
from django.utils import simplejson as json
from httplib2 import Http

userList = {}
count = 0


class User:
    def __init__(self, uid=0, name=u''):
        self.uid = uid
        self.name = name


class HttpMonitor:

    def user(self, cid=0):
        if not userList.get(cid):
            url = u"http://127.0.0.1:8000/cron/getAuthors?cid=%d" % cid
            userCatatoryList = []
            h = Http()
            resp, content = h.request(url, "GET")
            for item in json.loads(content).get("datas"):
                user = User(int(item.get("uid")), item.get("name"))
                userCatatoryList.append(user)
            if userCatatoryList:
                print 'this is init time'
                userList[cid] = userCatatoryList
            else:
                return User(2, u'user1')
        return random.choice(userList.get(cid))

    def postContent(self, uid, userName, title, content, date, cid, refSiteId, refId, refUrl):
        params = json.dumps({'datas': [
            {'uid': uid, 'userName': userName, 'title': title,
             'content': content, 'date': date,
             'cid': cid, 'refSiteId': refSiteId, 'refId': refId, 'refUrl': refUrl}
        ]})
        headers = {"Content-type": "application/json", "Accept": "text/plain", "User-Agent": "Magic Browser"}
        h = Http()
        resp, content = h.request("http://127.0.0.1:8000/cron/add", "POST", body=params, headers=headers)
        print resp
        print content


class WebPageContent:
    def __init__(self, url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()

    def getData(self):
        return self.htmlSource

    def writeData(self, fileName):
        fileContent = ""
        fSock = open(fileName, "wb")
        fSock.write(fileContent)
        fSock.close()


class BookParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.deep = 0
        self.deepBook = 1
        self.deepBookInfo = 2
        self.deepTitle = 3
        self.deepAuthor = 3
        self.deepIntro = 3
        self.deepUpdateTime = 4
        self.deepLastPostTitle = 4
        self.deepLastPostContent = 4
        #done
        self.title = u''
        #done
        self.intro = u''
        #done
        self.author = u''
        #done
        self.updateTime = u''
        self.category = u''
        self.lastPostContent = u''
        self.lastPostTitle = u''
        self.lastVipPostLink = u''
        self.lastVipPostTitle = u''
        self.lastVipPostContent = u''
        self.lastNotVipPostLink = u''
        self.lastNotVipPostTitle = u''
        self.lastNotVipPostContent = u''
        self.replies = []
        # book tag
        self.isBook = False
        #book info tag
        self.isBookInfo = False
        #title tag
        self.isTitle = False
        self.isTitleName = False
        #intro tag
        self.isIntro = False
        #author tag
        self.isAuthor = False
        self.isAuthorName = False
        #update tag
        self.isUpdateTime = False
        self.isUpdateTimeDiv = False
        #remove tag
        self.isNotProcess = False

        self.isLastPostContent = False
        self.isLastVipPost = False
        self.isLastVipPostTitle = False
        self.isLastVipPostTitleName = False
        self.isLastVipPostContent = False
        self.isLastVipPostContentLink = False
        self.isLastNotVipPost = False
        self.isLastNotVipPostTitle = False
        self.isLastNotVipPostTitleName = False
        self.isLastNotVipPostContent = False
        self.isLastNotVipPostContentLink = False

    def handle_data(self, text):
        if self.isTitleName and self.deep == self.deepTitle:
            self.title = text.strip("\r\n").strip()
        if self.isAuthorName and self.deep == self.deepTitle:
            self.author = text.strip("\r\n").strip()
        if self.isUpdateTime:
            self.updateTime = text.strip("\r\n").strip().replace(u'更新时间：', '')
        if self.isIntro and not self.isNotProcess:
            self.intro += text.strip("\r\n").strip(u"　").strip()
        if self.isLastVipPostTitleName:
            self.lastVipPostTitle = text.strip("\r\n").strip()
        if self.isLastVipPostContentLink:
            self.lastVipPostContent += text.strip("\r\n").strip(u"　").strip()

    def start_div(self, attrs):
        contentDiv = [v for k, v in attrs if k == 'id' and v == 'mainContent']
        if contentDiv:
            self.isBook = True
            self.deep += 1

        bookInfoDiv = [v for k, v in attrs if k == 'id' and v == 'divBookInfo']
        if bookInfoDiv:
            self.isBookInfo = True
            self.deep += 1

        if self.isBookInfo:
            if not self.title:
                titleDepthDiv = [v for k, v in attrs if k == 'class' and v == 'title']
                if titleDepthDiv:
                    self.isTitle = True
                    self.isAuthor = True

            if not self.updateTime:
                updateTimeDiv = [v for k, v in attrs if k == 'class' and v == 'tabs']
                if updateTimeDiv:
                    self.isUpdateTimeDiv = True
                    self.deep += 1

                if self.isUpdateTimeDiv:
                    updateTime = [v for k, v in attrs if k == 'class' and v == 'right']
                    if updateTime:
                        self.isUpdateTime = True
                        self.deep += 1

            if not self.intro:
                introDiv = [v for k, v in attrs if k == 'class' and v == 'txt']
                if introDiv:
                    self.isIntro = True
                    self.deep += 1

        lastPostInfoDiv = [v for k, v in attrs if k == 'class' and v == 'bookupdata like_box']
        if lastPostInfoDiv:
            self.isLastPostContent = True
            self.deep += 1

        if self.isLastPostContent:
            isVip = [v for k, v in attrs if k == 'id' and v == 'readV']
            if isVip:
                self.isLastVipPost = True
                self.deep += 1

        if self.isLastVipPost and self.deep == self.deepLastPostTitle - 1:
            isVipTitle = [v for k, v in attrs if k == 'class' and v == 'title']
            if isVipTitle:
                self.isLastVipPostTitle = True
                self.deep += 1
            isVipContent = [v for k, v in attrs if k == 'class' and v == 'cont']
            if isVipContent:
                self.isLastVipPostContent = True
                self.deep += 1
        #

    def end_div(self):
        if self.isBook and self.deep == self.deepBook - 1:
            self.isBook = False
        if self.isBookInfo and self.deep == self.deepBookInfo - 1:
            self.isBookInfo = False
        if self.isUpdateTime and self.deep == self.deepUpdateTime:
            self.isUpdateTimeDiv = False
            self.deep -= 1
            self.isUpdateTime = False
            self.deep -= 1
        if self.isIntro and self.deep == self.deepIntro:
            self.isIntro = False
            self.deep -= 1
            # this is for book info end
            self.deep -= 1
        if self.isLastVipPostTitle and self.deep == self.deepLastPostTitle:
            self.isLastVipPostTitle = False
            self.deep -= 1

    def start_h1(self, attrs):
        if self.isTitle and self.deep == self.deepBookInfo:
            self.isTitleName = True
            self.deep += 1

    def end_h1(self):
        if self.isTitleName and self.deep == self.deepTitle:
            self.isTitle = False
            self.isTitleName = False
            self.deep -= 1

    def start_a(self, attrs):
        if self.isAuthor and self.deep == self.deepBookInfo:
            authorName = [v for k, v in attrs if k == 'target' and v == '_blank']
            if authorName:
                self.isAuthorName = True
                self.deep += 1
        if self.isLastVipPostTitle:
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                self.lastVipPostLink = linkUrl
            except IndexError:
                pass

        if self.isLastVipPostContent:
            self.isLastVipPostContentLink = True

    def end_a(self):
        if self.isAuthorName and self.deep == self.deepAuthor:
            self.isAuthor = False
            self.isAuthorName = False
            self.deep -= 1
        if self.isLastVipPostTitle and self.deep == self.deepLastPostTitle:
            self.isLastVipPostTitle = False
            self.deep -= 1
        if self.isLastVipPostContentLink and self.deep == self.deepLastPostTitle:
            self.isLastVipPostContentLink = False
            self.isLastVipPostContent = False
            self.isLastVipPost = False
            self.deep -= 1
            self.deep -= 1
            self.deep -= 1

    def start_b(self, attrs):
        if self.isIntro:
            removeTag = [v for k, v in attrs if k == 'id' and v == 'essactive']
            if removeTag:
                self.isNotProcess = True

    def end_b(self):
        if self.isIntro and self.isNotProcess:
            self.isNotProcess = False

    def start_span(self, attrs):
        if self.isIntro:
            removeTag = [v for k, v in attrs if k == 'id' and v == 'spanBambookPromotion']
            if removeTag:
                self.isNotProcess = True

    def end_span(self):
        if self.isIntro and self.isNotProcess:
            self.isNotProcess = False

    def start_font(self, attrs):
        if self.isLastVipPostTitle:
            self.isLastVipPostTitleName = True

    def end_font(self):
        if self.isLastVipPostTitleName:
            self.isLastVipPostTitleName = False


class BookInfo:
    def __init__(self, url, cid=0):
        self.cid = cid
        self.url = url
        self.fid = 0
        self.run()

    def setUp(self):
        pattern = re.compile(r'http://.*?/([0-9]+)\.aspx')
        m = pattern.match(self.url)
        if m:
            self.fid = int(m.group(1))
            # print self.fid

    def run(self):
        self.setUp()
        content = WebPageContent(self.url)
        parser = BookParser()
        parser.feed(content.getData())
        parser.close()
        # print u'作者：' + parser.author
        # print u'标题：' + parser.title
        # print u'简介：' + parser.intro
        # print u'时间：' + parser.updateTime
        # #print u'深度：%d' % parser.deep
        # print u'vip标题：' + parser.lastVipPostTitle
        # print u'vip链接：' + parser.lastVipPostLink
        # print u'vip内容：' + parser.lastVipPostContent
        hm = HttpMonitor()
        user = hm.user(self.cid)
        if user:
            global count
            count += 1
        hm.postContent(user.uid, user.name, parser.title, parser.intro, parser.updateTime, self.cid, 1, self.fid,
                       self.url)
        # print user.name
        # print user.uid

if __name__ == "__main__":
    BookInfo("http://www.qidian.com/Book/2517792.aspx")