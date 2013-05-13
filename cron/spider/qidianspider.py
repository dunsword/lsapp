# coding=utf-8
import sys
import os
import re
import urllib
import thread
import threading
import random
from sgmllib import SGMLParser
from httplib2 import Http
from django.utils import simplejson as json

reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")


'''
功能：目前采用抓取分类，然后按照分类进行抓取3页，然后对每页的每个链接抓取对应的信息
运行：直接运行文件，Spider类进行多线程分发，按照每个分类，进行不同的页面抓取（这里分类采用七点的大分类）
      Timer是根据不同的分类进行调用RecursionPage抓取页面包


'''

#全局变量
localDomain = u'http://127.0.0.1:8000'
#分类的对应，前面是起点的categoryId，后面对应接口的categoryId
categoryDict = {
    '1': 106, # 奇幻
    '21': 105, # 玄幻
    '2': 109, # 武侠
    '22': 110, # 仙侠
    '4': 103, # 都市
    '15': 104, # 青春 这个暂时先对应 言情
    #'5': xxx, # 历史 这个没法对应
    '6': 120, # 军事  这个暂时先对应 现代
    #'7': '', # 游戏
    #'8': '', # 竞技
    '9': 105, # 科幻
    #'10': '', # 灵异
    '12': 108, # 同人
    #'14': '', # 图文
    #'31': '', # 文学
    #'41': '', # 女生
}
#下一页的url
nextUrl = u''
#用户列表
userList = {}


class BookStoreData:
    def __init__(self):
        self.title = u""
        self.linkUrl = u""
        self.categoryUrl = u""
        self.categoryName = u""
        self.parentCategoryUrl = u""
        self.parentCategoryName = u""
        self.updateTime = u''


class User:
    def __init__(self, uid=0, name=u''):
        self.uid = uid
        self.name = name


class WebPageContent:
    def __init__(self, url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()

    def getData(self):
        return self.htmlSource


class HttpMonitor:
    def user(self, cid=0):
        if not userList.get(cid):
            url = u"%s/cron/getAuthors?cid=%d" % (localDomain, cid)
            userCategoryList = []
            h = Http()
            resp, content = h.request(url, "GET")
            for item in json.loads(content).get("datas"):
                user = User(int(item.get("uid")), item.get("name"))
                userCategoryList.append(user)
            if userCategoryList:
                print 'this is init time'
                userList[cid] = userCategoryList
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
        url = u"%s/cron/add" % localDomain
        resp, content = h.request(url, "POST", body=params, headers=headers)
        print resp
        print content


class BookStoreParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.bookStoreData = None
        self.bookCategoryList = []
        self.isContent = False
        self.isTitle = False
        self.isTitleSpan = False
        self.isTitleDiv = False
        self.isCategory = False
        self.isCategoryDiv = False
        self.isNextDiv = False
        self.hasPrevious = False
        self.hasNextUrl = False
        self.isUpdateTime = False

    def getBookList(self):
        return self.bookCategoryList

    def handle_data(self, text):
        if self.isTitle:
            title = text.strip("\r\n").strip()
            self.bookStoreData.title = title
        if self.isCategory:
            if self.bookStoreData.parentCategoryName:
                self.bookStoreData.categoryName = text.strip("\r\n").strip()
            else:
                self.bookStoreData.parentCategoryName = text.strip("\r\n").strip()
        if self.isUpdateTime:
            self.bookStoreData.updateTime = u'20%s' % text.strip("\r\n").strip()

    def start_div(self, attrs):
        contentDiv = [v for k, v in attrs if k == 'class' and v == 'swz']
        if contentDiv:
            self.bookStoreData = BookStoreData()
            self.bookCategoryList.append(self.bookStoreData)
            self.isContent = True

        titleDiv = [v for k, v in attrs if k == 'class' and v == 'swb']
        if titleDiv:
            self.isTitleDiv = True

        catDiv = [v for k, v in attrs if k == 'class' and v == 'swa']
        if catDiv:
            self.isCategoryDiv = True

        if not nextUrl:
            nextUrlDiv = [v for k, v in attrs if k == 'class' and v == 'storelistbottom']
            if nextUrlDiv:
                self.isNextDiv = True

        updateDiv =  [v for k, v in attrs if k == 'class' and v == 'swe']
        if updateDiv:
            self.isUpdateTime = True

    def end_div(self):
        if self.isContent:
            self.isContent = False
        if self.isCategoryDiv:
            self.isCategoryDiv = False
        if self.isNextDiv:
            self.isNextDiv = False
        if self.isUpdateTime:
            self.isUpdateTime = False

    def start_span(self, attrs):
        if self.isTitleDiv:
            titleSpan = [v for k, v in attrs if k == 'class' and v == 'swbt']
            if titleSpan:
                self.isTitleSpan = True

    def end_span(self):
        if self.isTitleDiv:
            self.isTitleDiv = False

    def start_a(self, attrs):
        if self.isTitleSpan:
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                self.isTitle = True
                self.bookStoreData.linkUrl = linkUrl
            except IndexError:
                pass
        if self.isCategoryDiv:
            try:
                catLink = [v for k, v in attrs if k == 'href'][0]
                self.isCategory = True
                if self.bookStoreData.parentCategoryUrl:
                    self.bookStoreData.categoryUrl = catLink
                else:
                    self.bookStoreData.parentCategoryUrl = catLink
            except IndexError:
                pass
        if self.isNextDiv:
            if self.hasPrevious:
                global nextUrl
                nextUrl = [v for k, v in attrs if k == 'href'][0]
                self.hasNextUrl = True
            if not self.hasPrevious:
                previousLink = [v for k, v in attrs if k == 'class' and v == 'f_s']
                if previousLink:
                    self.hasPrevious = True

    def end_a(self):
        if self.isTitleSpan:
            self.isTitleSpan = False
            self.isTitle = False
        if self.isCategory:
            self.isCategory = False
        if self.hasNextUrl:
            self.hasPrevious = False


class BookInfoParser(SGMLParser):
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


class RecursionPage:
    def __init__(self, url, cid=0, startPage=1, totalPage=1):
        self.cid = cid
        self.url = url
        self.start = startPage
        self.end = totalPage
        self.run()

    def reset(self):
        global nextUrl
        nextUrl = u''

    def run(self):
        self.reset()
        content = WebPageContent(self.url)
        pattern = re.compile(r'http://.*?/')
        fidPattern = re.compile(r'http://.*?/([0-9]+)\.aspx')
        match = pattern.match(self.url)
        domain = ''
        if match:
            domain = match.group()
            domain = domain[0: int(len(domain)) - 1]
        parser = BookStoreParser()
        parser.feed(content.getData())
        parser.close()
        bookContent = parser.getBookList()
        if bookContent:
            for item in bookContent:
                lMatch = pattern.match(item.linkUrl)
                if lMatch:
                    url = item.linkUrl
                else:
                    url = domain + item.linkUrl

                m = fidPattern.match(url)
                if m:
                    print int(m.group(1))
                print url, self.cid, item.updateTime
                # BookInfo(url, self.cid)
            if self.start < self.end:
                if nextUrl:
                    RecursionPage(nextUrl, self.cid, self.start + 1, self.end)
        # thread.exit_thread()


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

    def run(self):
        self.setUp()
        content = WebPageContent(self.url)
        parser = BookInfoParser()
        parser.feed(content.getData())
        parser.close()
        hm = HttpMonitor()
        user = hm.user(self.cid)
        if user:
            # print parser.title, user.name, self.cid, self.fid
            hm.postContent(user.uid, user.name, parser.title, parser.intro, parser.updateTime, self.cid, 1, self.fid,
                           self.url)


class Timer(threading.Thread):
    def __init__(self, url, cid):
        threading.Thread.__init__(self)
        self.url = url
        self.cid = cid
        self.thread_stop = False

    def run(self):
        print self.url, self.cid
        RecursionPage(self.url, self.cid)


class Spider():
    for key in categoryDict:
        url = u'http://all.qidian.com/Book/BookStore.aspx?ChannelId=%s' % key
        RecursionPage(url, categoryDict[key])
        # 如果不是多线程，按照上面来，如果是多线程，则按照下面来，
        # 下面开启后，需要在RecursionPage中开启thread.exit_thread()
        # thread = Timer(url, categoryDict[key])
        # thread.start()


if __name__ == "__main__":
    Spider()