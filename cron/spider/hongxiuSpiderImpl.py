# coding=utf-8

import re
from sgmllib import SGMLParser
from api.docAuthor import Author
from api.docfetcher import DocumentFetcher, DocItem, SourceInfo, DocumentList
from cron.spider.spider import SpiderUrlConvert, WebPageContent, Category

#分类的对应，前面是起点的categoryId，后面对应接口的categoryId
categoryDict = {
    # '':101,#穿越
    # '':102,#重生
    # '':103,#都市
    # '':104,#言情
    # '':105,#玄幻
    # '':106,#奇幻
    # '':107,#耽美
    # '':108,#同人
    # '':109,#武侠
    # '':110,#仙侠
    # '':111,#末世
    # '':112,#甜宠
    # '':113,#女主
    # '':114,#修仙
    # '':115,#腹黑
    # '':116,#空间
    # '':117,#婚后
    # '':118,#女强
    # '':119,#女尊
    # '':120,#现代
    # '':121,#师徒
    # '':122,#清穿
    # '':123,#教授
    # '':124,#帝王
    # '':125,#架空
    # '':126,#姐弟
    # '':127,#小白
    # '':128,#民国
    # '':129,#修真
    # '':130,#复仇
    # '':131,#宫斗
    # '':132,#黑道
    # '':133,#总裁
    # '':134,#婚恋
    # '':135,#豪门
    # '':136,#宠文

    'zl1_8': 101, # 穿越时空
    'zl1_3': 133, # 总裁豪门
    'zl1_6': 125, # 古典架空
    # 'zl1_1': 0, # 青春校园
    'zl1_9': 120, # 都市高干
    'zl1_2': 120, # 白领职场
    'zl1_4': 119, # 女尊王朝
    'zl1_7': 107, # 耽美同人
    'zl1_10': 105, # 玄幻仙侠
    'zl2_2': 135, # 商场小说
    'zl2_3': 120, # 官场小说
    'zl2_4': 134, # 婚姻家庭
    'zl2_5': 103, # 职场励志
    # 'zl11_1': 0, # 纪实文学
    # 'zl11_2': 0, # 乡土文学
    # 'zl11_3': 0, # 儿童文学
    # 'zl11_4': 0, # 文史大观
    # 'zl11_5': 0, # 科普生活
    '1': 104, # 言情小说
    '2': 103, # 都市小说
    '3': 109, # 武侠仙侠
    '4': 105, # 玄幻奇幻
    # '5': 0, # 惊悚小说
    # '6': 0, # 悬疑小说
    # '7': 0, # 历史小说
    # '8': 0, # 军事小说
    # '9': 0, # 科幻小说
    # '10': 0, # 网游小说
    # '11': 0, # 社科人文
}


class BookStoreData:
    """
    解析小说列表
    获得一个分类下的最新小说列表。
    """

    def __init__(self):
        self.title = u''
        self.linkUrl = u''
        self.author = u''
        self.updateTime = u''
        self.wordNum = 0
        self.readNum = 0
        self.lastPostTitle = u''
        self.lastPostUrl = u''
        self.endStatus = 0


class BookListByCategoryParser(SGMLParser):
    """
    解析根据category的类别获取的html内容。
    """

    def reset(self):
        SGMLParser.reset(self)
        self.bookStoreData = None
        self.bookList = []
        self.nextUrl = u''
        self.isBookList = False
        self.isTitleInfo = False
        self.isTitleStrong = False
        self.isTitle = False
        self.isAuthorSpan = False
        self.isAuthor = False
        self.isCountInfo = False
        self.isWordNum = False
        self.isReadNum = False
        self.isUpdateTime = False
        self.isLastPost = False
        self.isLastPostTitle = False
        self.isPageInfo = False
        self.hasCurrentPage = False
        self.isNextPage = False
        self.isEndDT = False
        self.isEndStatus = False

    def getBookList(self):
        return self.bookList

    def handle_data(self, text):
        if self.isTitle:
            self.bookStoreData.title = text.strip("\r\n").strip()
        if self.isAuthor:
            self.bookStoreData.author = text.strip("\r\n").strip()
        if self.isWordNum:
            wordNum = text.strip("\r\n").strip(u"万").strip()
            self.bookStoreData.wordNum = int(float(wordNum) * 10000)
        if self.isReadNum:
            self.bookStoreData.readNum = int(text.strip("\r\n").strip())
        if self.isUpdateTime:
            self.bookStoreData.updateTime = text.strip("\r\n").strip()
        if self.isLastPostTitle:
            self.bookStoreData.lastPostTitle = text.strip("\r\n").strip()
        if self.isEndStatus:
            endName = text.strip("\r\n").strip()
            if not cmp(endName, "全本"):
                self.bookStoreData.endStatus = 1

    def start_div(self, attrs):
        if self.isBookList:
            titleInfo = [v for k, v in attrs if k == 'class' and v == 'name']
            if titleInfo:
                self.isTitleInfo = True
                self.bookStoreData = BookStoreData()
                self.bookList.append(self.bookStoreData)
            countInfo = [v for k, v in attrs if k == 'class' and v == 'num']
            if countInfo:
                self.isCountInfo = True

    def end_div(self):
        if self.isTitleInfo:
            self.isTitleInfo = False
        if self.isCountInfo:
            self.isCountInfo = False

    def start_a(self, attrs):
        if self.isTitleStrong:
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                self.isTitle = True
                self.bookStoreData.linkUrl = linkUrl
            except IndexError:
                pass
        if self.isAuthorSpan:
            self.isAuthor = True

        if self.isLastPost:
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                self.isLastPostTitle = True
                self.bookStoreData.lastPostUrl = linkUrl
            except IndexError:
                pass

        if self.isNextPage:
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                self.nextUrl = linkUrl
            except IndexError:
                pass

    def end_a(self):
        if self.isTitle:
            self.isTitle = False

        if self.isAuthor:
            self.isAuthor = False

        if self.isLastPostTitle:
            self.isLastPostTitle = False

    def start_ul(self, attrs):
        bookList = [v for k, v in attrs if k == 'id' and v == 'BookList']
        if bookList:
            self.isBookList = True

        pageInfo = [v for k, v in attrs if k == 'id' and v == 'htmlPage']
        if pageInfo:
            self.isPageInfo = True

    def end_ul(self):
        if self.isBookList:
            self.isBookList = False
        if self.isPageInfo:
            self.isPageInfo = False

    def start_strong(self, attrs):
        if self.isTitleInfo:
            self.isTitleStrong = True

    def end_strong(self):
        if self.isTitleStrong:
            self.isTitleStrong = False

    def start_span(self, attrs):
        if self.isTitleInfo:
            self.isAuthorSpan = True
        if self.isCountInfo:
            if self.bookStoreData and not self.bookStoreData.wordNum:
                self.isWordNum = True
            if self.bookStoreData and self.bookStoreData.wordNum and not self.bookStoreData.readNum:
                self.isReadNum = True

    def end_span(self):
        if self.isAuthorSpan:
            self.isAuthorSpan = False
        if self.isWordNum:
            self.isWordNum = False
        if self.isReadNum:
            self.isReadNum = False

    def start_dt(self, attrs):
        if self.isBookList:
            self.isLastPost = True
            self.isEndDT = True

    def end_dt(self):
        if self.isLastPost:
            self.isLastPost = False
        if self.isEndDT:
            self.isEndDT = False

    def start_i(self, attrs):
        if self.isEndDT:
            self.isEndStatus = True

    def end_i(self):
        if self.isEndStatus:
            self.isEndStatus = False

    def start_em(self, attrs):
        if self.isLastPost:
            self.isUpdateTime = True

    def end_em(self):
        if self.isUpdateTime:
            self.isUpdateTime = False

    def start_li(self, attrs):
        if self.isPageInfo:
            currentPage = [v for k, v in attrs if k == 'id' and v == 'pagenow']
            if currentPage:
                self.hasCurrentPage = True
            if self.hasCurrentPage:
                nextPage = [v for k, v in attrs if k == 'class' and v == 'np']
                if nextPage:
                    self.isNextPage = True

    def end_li(self):
        if self.isNextPage:
            self.isNextPage = False
            self.hasCurrentPage = False


class BookInfoEncodeParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.hasMatch = False
        self.readNum = 0
        self.wordNum = 0
        self.isScript = 0
        self.hasScript = False
        self.isDomain = False
        self.domain = u''
        self.listUrl = u''

    def start_meta(self, attrs):
        if not self.hasMatch:
            type = [v for k, v in attrs if k == 'http-equiv' and v == 'Content-Type']
            content = [v for k, v in attrs if k == 'content' and v == 'text/html; charset=utf-8']
            if type and content:
                self.hasMatch = True

    def start_script(self, attrs):
        if not self.hasScript:
            hasScript = [v for k, v in attrs if k == 'charset' and v == 'GB2312']
            if hasScript:
                try:
                    srcLink = [v for k, v in attrs if k == 'src'][0]
                    self.hasScript = True
                    jsContent = WebPageContent(srcLink)
                    readNumPattern = re.compile(r'.*?a_yuedus="([0-9]+)";.*?')
                    readMatch = readNumPattern.match(jsContent.getData())
                    if readMatch:
                        self.readNum = int(readMatch.group(1))
                    wordNumPattern = re.compile(r'[\s\S]*?nrbyte="([0-9]+)";[\s\S]*?')
                    wordMatch = wordNumPattern.match(jsContent.getData())
                    if wordMatch:
                        self.wordNum = int(wordMatch.group(1))
                except IndexError:
                    pass

    def start_div(self, attrs):
        if not self.domain:
            hasDomain = [v for k, v in attrs if k == 'class' and v == 'wrapper_src']
            if hasDomain:
                self.isDomain = True

    def end_div(self):
        if self.isDomain:
            self.isDomain = False

    def start_a(self, attrs):
        if not self.domain and self.isDomain:
            try:
                domain = [v for k, v in attrs if k == 'href'][0]
                if not cmp('http://www.hongxiu.com/', domain):
                    self.domain = u'http://novel.hongxiu.com/'
                else:
                    self.domain = domain
            except Exception:
                pass

        if not self.listUrl:
            listUrl = [v for k, v in attrs if k == 'id' and v == 'htmlmulu']
            if listUrl:
                try:
                    list = [v for k, v in attrs if k == 'href'][0]
                    if self.domain:
                        self.listUrl = self.domain[0:len(self.domain) - 1] + list
                    else:
                        self.listUrl = u'http://novel.hongxiu.com%s' % list
                except IndexError:
                    pass


class BookInfoParser(SGMLParser):
    """
    accroding
    """

    def reset(self):
        SGMLParser.reset(self)
        self.wordNum = 0
        self.intro = u''
        self.isIntro = False
        self.isWordNum = False

    def handle_data(self, text):
        if self.isIntro:
            self.intro += text.strip("\r\n").strip()
        if self.isWordNum:
            self.wordNum = int(text.strip("\r\n").strip())

    def start_span(self, attrs):
        wordNum = [v for k, v in attrs if k == 'id' and v == 'ajZiShu']
        if wordNum:
            self.isWordNum = True

    def end_span(self):
        if self.isWordNum:
            self.isWordNum = False

    def start_h3(self, attrs):
        intro = [v for k, v in attrs if k == 'id' and v == 'htmljiashao']
        if intro:
            self.isIntro = True

    def end_h3(self):
        if self.isIntro:
            self.isIntro = False


class BookListData:
    def __init__(self):
        self.title = u""
        self.linkUrl = u""
        self.isVip = False
        self.updateTime = u""


class BookChapterListParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.bookTitleList = None
        self.bookList = []
        self.isContent = False
        self.isLi = False
        self.isLink = False
        self.isDate = False
        self.isFont = False
        self.pattern = re.compile(r"http://[\s\S]*")

    def getTitleList(self):
        return self.bookList

    def handle_data(self, text):
        if self.isLink:
            self.bookTitleList.title = text.strip("\r\n").strip("' target='_blank'>").strip()
        if self.isFont:
            self.bookTitleList.isVip = True
        if self.isDate:
            self.bookTitleList.updateTime = text.strip("\r\n").strip()

    def start_div(self, attrs):
        isContent = [v for k, v in attrs if k == 'id' and v == 'htmlList']
        if isContent:
            self.isContent = True

    def end_div(self):
        if self.isContent:
            self.isContent = False

    def start_li(self, attrs):
        if self.isContent:
            self.isLi = True
            self.bookTitleList = BookListData()
            self.bookList.append(self.bookTitleList)

    def end_li(self):
        if self.isLi:
            self.isLi = False

    def start_a(self, attrs):
        if self.isLi:
            self.isLink = True
            bookListUrl = u""
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                bookListUrl = linkUrl
            except IndexError:
                pass
            if bookListUrl:
                sm = self.pattern.match(bookListUrl)
                if not sm:
                    bookListUrl = u"http://novel.hongxiu.com%s" % bookListUrl
                self.bookTitleList.linkUrl = bookListUrl

    def end_a(self):
        if self.isLink:
            self.isLink = False

    def start_span(self, attrs):
        if self.isLi:
            self.isDate = True

    def end_span(self):
        if self.isDate:
            self.isDate = False

    def start_font(self, attrs):
        if self.isLi:
            isFont = [v for k, v in attrs if k == 'class' and v == 'isvip']
            if isFont:
                self.isFont = True

    def end_font(self):
        if self.isFont:
            self.isFont = False


class BookDetailParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.content = u''
        self.isP = False
        self.isContent = False

    def handle_data(self, text):
        if self.isP:
            self.content += text.strip("\r\n").strip(u"　").strip()

    def start_div(self, attrs):
        contentDiv = [v for k, v in attrs if k == 'id' and v == 'htmlContent']
        if contentDiv:
            self.isContent = True

    def end_div(self):
        if self.content and self.isContent:
            self.isContent = False

    def start_p(self, attrs):
        if self.isContent:
            self.isP = True

    def end_p(self):
        if self.isP:
            self.isP = False


class HXCategory(Category):
    def getCategoryName(self, sourceCategoryName):
        """
        :param sourceCategoryName:
        :return:TODO this need return correct cid
        """
        return 104

    def getCategoryId(self, sourceCategoryId):
        """
        according to hx site category id to get self site category id
        :param sourceCategoryId:
        :return: self site category id
        """
        cid = categoryDict[sourceCategoryId]
        if cid:
            return cid
        return 104


class HXURLConvert(SpiderUrlConvert):
    def convertBookUrl(self, tid):
        return u"http://novel.hongxiu.com/a/%d/list.shtml" % tid

    def convertBookListUrl(self, page):
        """
        :param page:
        :return:TODO
        """
        return u'http://www.hongxiu.com/novel/s/%s_1_order9.html' % page

    def convertBookListUrl(self, cid, page=1):
        return u'http://www.hongxiu.com/novel/s/%s_%d_order9.html' % (cid, page)


class HXDocumentFetcher(DocumentFetcher):
    def getDocumentPage(self, tid, page=1):
        """
        获取一个文章页的接口，根据每个站点实现
        返回DocItemDetailPage对象
        """
        listUrl = HXURLConvert().convertBookUrl(tid)
        content = WebPageContent(listUrl)
        parser = BookChapterListParser()
        parser.feed(content.getData())
        if page <= 0:
            page = 1
        if parser.getTitleList() and len(parser.getTitleList()) >= page:
            item = parser.getTitleList()[page - 1]
            if not item.isVip:
                content = WebPageContent(item.linkUrl)
                parser = BookDetailParser()
                parser.feed(content.getData())
                parser.close()
                print parser.content
            else:
                print "this is vip"
        pass

    def getLatestDocumentList(self, sid, size):
        listUrl = HXURLConvert().convertBookListUrl(sid, size)
        content = WebPageContent(listUrl)
        parser = BookListByCategoryParser()
        parser.feed(content.getData().decode('gbk', 'ignore').encode('utf-8'))
        parser.close()
        bookList = parser.getBookList()
        threadList = []
        cid = HXCategory().getCategoryId(sid)
        for item in bookList:
            tid = re.findall(r'.*/([0-9]+)/', item.linkUrl)
            if tid:
                tid = tid[0]
            subject = item.title
            url = item.linkUrl
            user = Author().getAuthorByCid(cid)
            """
            获取图书简介
            """
            parser = BookInfoParser()
            content = WebPageContent(item.linkUrl)
            encodeParser = BookInfoEncodeParser()
            encodeParser.feed(content.getData())
            encodeParser.close()
            if encodeParser.hasMatch:
                parser.feed(content.getData())
            else:
                parser.feed(content.getData().decode('gb2312', 'ignore').encode('utf-8'))
            parser.close()
            docItem = DocItem(tid=tid,
                              uid=user['uid'],
                              subject=subject,
                              url=url,
                              view_count=encodeParser.readNum,
                              content=parser.intro,
                              created_at=item.updateTime,
                              updated_at=item.updateTime)
            threadList.append(docItem)

        si = SourceInfo(source_id=sid, source_name="", source_desc="", site_id=1)
        return DocumentList(source_info=si, doc_list=threadList)


if __name__ == "__main__":
    # aa = HXDocumentFetcher().getLatestDocumentList("zl1_8", 1)
    # print ', '.join(['%s:%s' % item for item in aa.__dict__.items()])
    # group = re.findall(r'.*/([0-9]+)/', 'http://novel.hongxiu.com/a/568484/')
    # print group[0]

    bb = HXDocumentFetcher().getDocumentPage(616441, 100)