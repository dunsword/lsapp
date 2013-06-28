# coding=utf-8

import re
from sgmllib import SGMLParser
from datetime import datetime
from api.docAuthor import Author
from api.docfetcher import DocumentFetcher, DocItem, SourceInfo, DocumentList, RelyItem, DocItemDetailPage
from cron.spider.spider import SpiderUrlConvert, WebPageContent, Category

#分类的对应，前面是起点的categoryId，后面对应接口的categoryId
categoryDict = {
    '1': 106, # 奇幻
    '21': 105, # 玄幻
    '2': 109, # 武侠
    '22': 110, # 仙侠
    '4': 103, # 都市
    '15': 104, # 青春 这个暂时先对应 言情
    #'5': xxx,  # 历史 这个没法对应
    '6': 120, # 军事  这个暂时先对应 现代
    #'7': '',  # 游戏
    #'8': '',  # 竞技
    '9': 105, # 科幻
    #'10': '',  # 灵异
    '12': 108, # 同人
    #'14': '',  # 图文
    #'31': '',  # 文学
    #'41': '',  # 女生
}


class BookStoreData:
    """
    解析小说列表
    获得一个分类下的最新小说列表。
    """

    def __init__(self):
        self.title = u''
        self.linkUrl = u''


class BookListByCategoryParser(SGMLParser):
    """
    解析根据category的类别获取的html内容。
    """

    def reset(self):
        SGMLParser.reset(self)
        self.bookStoreData = None
        self.bookCategoryList = []
        self.isTitle = False
        self.isTitleSpan = False
        self.isTitleDiv = False
        self.pattern = re.compile(r'http://.*?/')

    def getBookList(self):
        return self.bookCategoryList

    def handle_data(self, text):
        if self.isTitle:
            title = text.strip("\r\n").strip()
            self.bookStoreData.title = title

    def start_div(self, attrs):
        contentDiv = [v for k, v in attrs if k == 'class' and v == 'swz']
        if contentDiv:
            self.bookStoreData = BookStoreData()
            self.bookCategoryList.append(self.bookStoreData)

        titleDiv = [v for k, v in attrs if k == 'class' and v == 'swb']
        if titleDiv:
            self.isTitleDiv = True

    def end_div(self):
        if self.isTitleDiv:
            self.isTitleDiv = False

    def start_span(self, attrs):
        if self.isTitleDiv:
            titleSpan = [v for k, v in attrs if k == 'class' and v == 'swbt']
            if titleSpan:
                self.isTitleSpan = True

    def end_span(self):
        if self.isTitleSpan:
            self.isTitleSpan = False

    def start_a(self, attrs):
        if self.isTitleSpan:
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                self.isTitle = True
                hasDomainUrl = self.pattern.match(linkUrl)
                if not hasDomainUrl:
                    linkUrl = u'%s' % linkUrl
                self.bookStoreData.linkUrl = linkUrl
            except IndexError:
                pass

    def end_a(self):
        if self.isTitle:
            self.isTitle = False


class BookInfoParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.title = u''
        self.intro = u''
        self.updateTime = u''
        self.category = u''
        self.readNum = 0
        # 如果已经完结了，则是1，否则是0
        self.endStatus = 0
        self.pattern = re.compile(r'http://all.qidian.com.*?ChannelId=([a-z0-9_]+).*?')
        # 完成度为1：标题，2：更新时间，3：阅读数；bookInfo关闭的标识
        self.bookCompletion = 0
        self.isNotProcess = False
        self.isBookInfo = False
        self.isCategoryDiv = False
        self.isTitleDiv = False
        self.isTitleH1 = False
        self.isTabsDiv = False
        self.isUpdateTimeDiv = False
        self.isIntroInfoDiv = False
        self.isDataDiv = False
        self.isReadNumTr = False
        self.isIntroDiv = False
        self.isEndStatusDiv = False
        self.isEndStatusTd = False
        self.isEndStatusCheck = False

    def handle_data(self, text):
        if self.isTitleH1:
            self.title = text.strip("\r\n").strip()
        if self.isUpdateTimeDiv:
            self.updateTime = text.strip("\r\n").strip().replace('更新时间：', '')
        if self.isReadNumTr and not self.isNotProcess:
            text = text.strip("\r\n").strip(u"　").strip()
            if text:
                self.readNum += int(text)
        if self.isIntroDiv and not self.isNotProcess:
            self.intro += u'%s\r\n\r\n' % text.strip("\r\n").strip()
        if self.isEndStatusTd:
            text = text.strip("\r\n").strip().strip()
            if self.isEndStatusCheck:
                if not cmp(text, "已经完本") or not cmp(text, "出版中"):
                    self.endStatus = 1
                    #完成度为6
                self.bookCompletion += 1
                self.isEndStatusCheck = False
            else:
                if not cmp(text, "写作进程："):
                    self.isEndStatusCheck = True

    def start_div(self, attrs):
        categoryDiv = [v for k, v in attrs if k == 'class' and v == 'page_site']
        if categoryDiv:
            self.isCategoryDiv = True
            #获取页面主要部分
        bookInfoDiv = [v for k, v in attrs if k == 'id' and v == 'divBookInfo']
        if bookInfoDiv:
            self.isBookInfo = True

        if self.isBookInfo:
            #获取标题节点
            titleDiv = [v for k, v in attrs if k == 'class' and v == 'title']
            if titleDiv:
                self.isTitleDiv = True
                #获取更新时间上层div节点
            tabsDiv = [v for k, v in attrs if k == 'class' and v == 'tabs']
            if tabsDiv:
                self.isTabsDiv = True
                #获取简介内容模块节点
            introDiv = [v for k, v in attrs if k == 'class' and v == 'intro']
            if introDiv:
                self.isIntroInfoDiv = True

        if self.isTabsDiv:
            #获取更新时间div节点
            updateTimeDIv = [v for k, v in attrs if k == 'class' and v == 'right']
            if updateTimeDIv:
                self.isUpdateTimeDiv = True
                #完成度为3
                self.bookCompletion += 1

        if self.isIntroInfoDiv:
            #获取书本数字方面的节点
            dataDiv = [v for k, v in attrs if k == 'class' and v == 'data']
            if dataDiv:
                self.isDataDiv = True
                #获取简介div节点
            introDiv = [v for k, v in attrs if k == 'class' and v == 'txt']
            if introDiv:
                self.isIntroDiv = True
                #完成度为5
                self.bookCompletion += 1

        endStatusDiv = [v for k, v in attrs if k == 'id' and v == 'bookdiv']
        if endStatusDiv:
            self.isEndStatusDiv = True

    def end_div(self):
        if self.bookCompletion == 6 and self.isBookInfo:
            self.bookCompletion = 0
            self.isBookInfo = False
        if self.isDataDiv:
            self.isDataDiv = False
        if self.isUpdateTimeDiv:
            self.isTabsDiv = False
            self.isUpdateTimeDiv = False
        if self.isIntroDiv:
            self.isIntroDiv = False
            self.isIntroInfoDiv = False
        if self.isCategoryDiv:
            self.isCategoryDiv = False
        if self.isEndStatusDiv:
            self.isEndStatusDiv = False

    def start_a(self, attrs):
        if self.isIntroDiv:
            self.isNotProcess = True
        if self.isCategoryDiv:
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                match = self.pattern.match(linkUrl)
                if match:
                    self.category = match.group(1)
                    #完成度为1
                    self.bookCompletion += 1
                    self.isCategoryDiv = False
            except IndexError:
                pass

    def end_a(self):
        if self.isIntroDiv and self.isNotProcess:
            self.isNotProcess = False

    def start_h1(self, attrs):
        if self.isTitleDiv:
            self.isTitleH1 = True
            #完成度为2
            self.bookCompletion += 1

    def end_h1(self):
        if self.isTitleH1:
            self.isTitleH1 = False

    def start_b(self, attrs):
        #阅读数b标签过滤
        if self.isIntroDiv:
            removeTag = [v for k, v in attrs if k == 'id' and v == 'essactive']
            if removeTag:
                self.isNotProcess = True
        if self.isReadNumTr:
            self.isNotProcess = True

    def end_b(self):
        if self.isIntroDiv and self.isNotProcess:
            self.isNotProcess = False
        if self.isReadNumTr and self.isNotProcess:
            self.isNotProcess = False

    def start_td(self, attrs):
        #阅读数tr标签
        if self.isDataDiv and self.bookCompletion == 3:
            self.isReadNumTr = True
            #完成度为4
            self.bookCompletion += 1
        if self.isEndStatusDiv and self.bookCompletion == 5:
            endStatusTd = [v for k, v in attrs if k == 'height' and v == '20']
            if endStatusTd:
                self.isEndStatusTd = True

    def end_td(self):
        if self.isReadNumTr:
            self.isReadNumTr = False
        if self.isEndStatusTd:
            self.isEndStatusTd = False


class BookListData:
    def __init__(self):
        self.title = u""
        self.linkUrl = u""
        self.isVip = False


class BookChapterListParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.bookTitleList = None
        self.bookList = []

        self.isContent = False
        self.isRelatedDiv = False
        self.isRelatedB = False
        self.isSkipContent = False
        self.isList = False
        self.isLink = False
        self.pattern = re.compile(r'http://.*?/')

    def getTitleList(self):
        return self.bookList

    def handle_data(self, text):
        if self.isLink:
            self.bookTitleList.title = text.strip("\r\n").strip("' target='_blank'>").strip()
        if self.isRelatedB:
            text = text.strip("\r\n").strip()
            if not cmp(text, "作品相关"):
                self.isSkipContent = True

    def start_div(self, attrs):
        isContent = [v for k, v in attrs if k == 'id' and v == 'content']
        if isContent:
            self.isContent = True

        if self.isContent:
            isRelated = [v for k, v in attrs if k == 'class' and v == 'title']
            if isRelated:
                self.isRelatedDiv = True
                self.isSkipContent = False

            if not self.isSkipContent:
                isList = [v for k, v in attrs if k == 'class' and v == 'list']
                if isList:
                    self.isList = True

    def end_div(self):
        if self.isList:
            self.isList = False
        if self.isRelatedDiv:
            self.isRelatedDiv = False

    def start_b(self, attrs):
        if self.isRelatedDiv:
            self.isRelatedB = True

    def end_b(self):
        if self.isRelatedB:
            self.isRelatedB = False

    def start_a(self, attrs):
        if self.isList:
            self.isLink = True
            self.bookTitleList = BookListData()
            self.bookList.append(self.bookTitleList)
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
                isVip = self.pattern.match(linkUrl)
                if isVip:
                    self.bookTitleList.isVip = True
                else:
                    linkUrl = u'http://read.qidian.com%s' % linkUrl
                self.bookTitleList.linkUrl = linkUrl
            except IndexError:
                pass

    def end_a(self):
        if self.isLink:
            self.isLink = False

    def start_span(self, attrs):
        endContent = [v for k, v in attrs if k == 'id' and v == 'stxt']
        if endContent and self.isContent:
            self.isContent = False


class BookDetailParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.updateTime = u''
        self.content = u''
        self.isUpdateTime = False
        self.isContent = False

    def handle_data(self, text):
        if self.isUpdateTime:
            self.updateTime = text.strip("\r\n").strip()

    def start_div(self, attrs):
        contentDiv = [v for k, v in attrs if k == 'id' and v == 'content']
        if contentDiv:
            self.isContent = True

    def end_div(self):
        if self.isContent:
            self.isContent = False

    def start_span(self, attrs):
        isUpdate = [v for k, v in attrs if k == 'id' and v == 'lblLastUpdateTime']
        if isUpdate:
            self.isUpdateTime = True

    def end_span(self):
        if self.isUpdateTime:
            self.isUpdateTime = False

    def start_script(self, attrs):
        if self.isContent:
            contentScript = [v for k, v in attrs if k == 'charset' and v == 'GB2312']
            if contentScript:
                try:
                    contentUrl = [v for k, v in attrs if k == 'src'][0]
                    if contentUrl:
                        c = WebPageContent(contentUrl)
                        self.content = c.getData().decode('GB2312', 'ignore').encode('utf-8').strip(
                            u"document.write('"). \
                            strip(u"<a href=http://www.qidian.com>起点中文网 www.qidian.com 欢迎广大书友光临阅读，"
                                  u"最新、最快、最火的连载作品尽在起点原创！</a>');").strip().replace('<p>', '\r\n\r\n');
                except IndexError:
                    pass


class QDCategory(Category):
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


class QDURLConvert(SpiderUrlConvert):
    def convertBookUrl(self, tid):
        return u"http://read.qidian.com/BookReader/%s.aspx" % tid

    def convertBookListUrl(self, page):
        """
        :param page:
        :return:TODO
        """
        return u'http://all.qidian.com/book/bookstore.aspx?PageIndex=%s' % page

    def convertBookInfoUrl(self, tid):
        return u'http://www.qidian.com/Book/%s.aspx' % tid

    def convertBookListUrl(self, cid, page=1):
        return u'http://all.qidian.com/book/bookstore.aspx?ChannelId=%s&PageIndex=%s' % (cid, page)


class QDDocumentParser():
    def getBookInfo(self, tid):
        linkUrl = QDURLConvert().convertBookInfoUrl(tid)

        parser = BookInfoParser()
        content = WebPageContent(linkUrl)
        parser.feed(content.getData())
        parser.close()
        sid = parser.category
        cid = QDCategory().getCategoryId(sid)
        user = Author().getAuthorByCid(cid)
        # noinspection PyBroadException
        try:
            updateTime = datetime.strptime(parser.updateTime, "%Y-%m-%d %H:%M")
        except Exception:
            updateTime = datetime.now()
            pass
        docItem = DocItem(tid=tid,
                          uid=user['uid'],
                          subject=parser.title,
                          url=linkUrl,
                          view_count=parser.readNum,
                          reply_count=len(self.getBookChapterList(tid)),
                          content=parser.intro,
                          created_at=updateTime,
                          updated_at=updateTime,
                          siteid=1)
        return docItem

    def getBookChapterList(self, tid):
        listUrl = QDURLConvert().convertBookUrl(tid)
        content = WebPageContent(listUrl)
        parser = BookChapterListParser()
        parser.feed(content.getData())
        titleList = []
        if parser.getTitleList():
            titleList = parser.getTitleList()
        return titleList


class QDDocumentFetcherImpl(DocumentFetcher):
    def getDocumentPage(self, tid, page=1):
        """
        获取一个文章页的接口，根据每个站点实现
        返回DocItemDetailPage对象
        :param tid:
        :param page:
        """
        titleList = QDDocumentParser().getBookChapterList(tid)
        page = int(page)
        if page <= 0:
            page = 1

        replyList = []
        user = Author().getAuthorByCid(102)
        docItem = QDDocumentParser().getBookInfo(tid)
        chapterContent = u''
        if titleList:
            if len(titleList) >= page:
                item = titleList[page - 1]

                pid = re.findall(r'http://.*([0-9]+),([0-9]+)\.aspx', item.linkUrl)
                if pid:
                    pid = pid[0][1]
                if not item.isVip:
                    content = WebPageContent(item.linkUrl)
                    parser = BookDetailParser()
                    parser.feed(content.getData())
                    parser.close()
                    chapterContent = parser.content

                replyItem = RelyItem(
                    rid=pid,
                    uid=user['uid'],
                    subject=item.title,
                    content=chapterContent,
                    is_chapter=1,
                    replyUrl=item.linkUrl,
                )
                replyList.append(replyItem)
        return DocItemDetailPage(docItem=docItem, page_number=page, reply_list=replyList)

    def getLatestDocumentList(self, sid, size):
        listUrl = QDURLConvert().convertBookListUrl(sid, size)
        content = WebPageContent(listUrl)
        parser = BookListByCategoryParser()
        parser.feed(content.getData())
        parser.close()
        bookList = parser.getBookList()
        threadList = []
        for item in bookList:
            tid = re.findall(r'.*/([0-9]+)\.aspx', item.linkUrl)
            if tid:
                tid = tid[0]
                threadList.append(QDDocumentParser().getBookInfo(tid))

        si = SourceInfo(source_id=sid, source_name="", source_desc="", site_id=2)
        return DocumentList(source_info=si, doc_list=threadList)

    def getLatestDocuentList(self,size):
        """
        获得站点排行榜的文章列表
        返回DocumentList对象
        """
        pass

    def getDocumentDetailByTid(self, tid):
        docItem = QDDocumentParser().getBookInfo(tid)
        si = SourceInfo(source_id=tid, source_name="", source_desc="", site_id=2)
        return DocumentList(source_info=si, doc_list=[docItem])


QDDocumentFetcher = QDDocumentFetcherImpl()

if __name__ == "__main__":
    # bb = QDDocumentParser().getBookChapterList(2652171)
    QDDocumentFetcher.getLatestDocumentList(22, 1)