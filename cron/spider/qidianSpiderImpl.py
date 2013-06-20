# coding=utf-8
import logging
import sys
import re,datetime
import os
import urllib
import random
import sqlite3
from sgmllib import SGMLParser
from httplib2 import Http
from django.utils import simplejson as json

from spider import  Category,SpiderUrlConvert,WebPageContent
from api.docfetcher import DocumentFetcher,RelyItem,DocItem,DocItemDetailPage,DocumentList,SourceInfo
from api.docAuthor import Author

#分类的对应，前面是起点的categoryId，后面对应接口的categoryId
categoryDict = {
    # '9':101,#穿越
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



     1: 106, # 奇幻
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

class BookStoreData:
    def __init__(self):
        self.title = u""
        self.linkUrl = u""
        self.categoryUrl = u""
        self.categoryName = u""
        self.parentCategoryUrl = u""
        self.parentCategoryName = u""
        self.updateTime = u''
        self.totalCount = 0


class BookListByCategoryParser(SGMLParser):
    """
    解析小说列表
    获得一个分类下的最新小说列表。
    """
    def reset(self):
        SGMLParser.reset(self)
        self.bookStoreData = None
        self.bookCategoryList = []
        self.bookBaseUrl = u''
        self.nextUrl = u''
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
        self.isTotalCount = False

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
        if self.isTotalCount:
            self.bookStoreData.totalCount = int(text.strip("\r\n").strip())

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

        if not self.nextUrl:
            nextUrlDiv = [v for k, v in attrs if k == 'class' and v == 'storelistbottom']
            if nextUrlDiv:
                self.isNextDiv = True

        updateDiv = [v for k, v in attrs if k == 'class' and v == 'swe']
        if updateDiv:
            self.isUpdateTime = True
        totalCountDiv = [v for k, v in attrs if k == 'class' and v == 'swc']
        if totalCountDiv:
            self.isTotalCount = True

    def end_div(self):
        if self.isContent:
            self.isContent = False
        if self.isCategoryDiv:
            self.isCategoryDiv = False
        if self.isNextDiv:
            self.isNextDiv = False
        if self.isUpdateTime:
            self.isUpdateTime = False
        if self.isTotalCount:
            self.isTotalCount = False

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
                self.nextUrl = [v for k, v in attrs if k == 'href'][0]
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

    def start_base(self, attrs):
        try:
            linkUrl = [v for k, v in attrs if k == 'href'][0]
            self.bookBaseUrl = linkUrl
        except IndexError:
            pass


class BookListData:
    def __init__(self):
        self.title = u""
        self.linkUrl = u""

class BookChapterListParser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.bookTitleList = None
        self.bookList = []
        self.isList = False
        self.isLink = False
        self.isContent = False

    def getTitleList(self):
        return self.bookList

    def handle_data(self, text):
        if self.isLink:
            self.bookTitleList.title = text.strip("\r\n").strip("' target='_blank'>").strip()

    def start_div(self, attrs):
        isContent = [v for k, v in attrs if k == 'id' and v == 'content']
        if isContent:
            self.isContent = True

        if self.isContent:
            isList = [v for k, v in attrs if k == 'class' and v == 'list']
            if isList:
                self.isList = True
            if self.isList:
                self.bookTitleList = BookListData()
                self.bookList.append(self.bookTitleList)

    def end_div(self):
        if self.isList:
            self.isList = False

    def start_a(self, attrs):
        if self.isList:
            self.isLink = True
            self.bookTitleList = BookListData()
            self.bookList.append(self.bookTitleList)
            try:
                linkUrl = [v for k, v in attrs if k == 'href'][0]
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
    """
    获得小说具体的章节内容。
    """
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
                                  u"最新、最快、最火的连载作品尽在起点原创！</a>');").strip().replace(u'　', u'');
                except IndexError:
                    pass




class QDCategory(Category):

    def getCategoryName(self,sourceCategoryName):
        """ 先返回言情 """
        return 104

    def getCategoryId(self,sourceCategoryId):
        cid = categoryDict[sourceCategoryId]
        if cid:
            return cid
        return 104

class QDURLConvert(SpiderUrlConvert):

    def convertBookUrl(self,tid):
        return u"http://read.qidian.com/BookReader/%d.aspx" % tid

    def convertChapterDetailUrl(self,tid,pid):
         return u"http://read.qidian.com/BookReader/%d,%d.aspx" %(tid,pid)

    def convertBookListUrl(self,page):
        """
        获得起点的会员点击排行榜的月榜
        """
        return u"http://top.qidian.com/Book/TopDetail.aspx?TopType=%d&Time=2" & page

    def convertBookListUrl(self,cid,page):
        return u'http://all.qidian.com/Book/BookStore.aspx?ChannelId=%s' % cid

# BOOK_CHAPTER_LIST 全局变量存储所有解析过的图书的章节信息，如果不存在，需要重新解析获得
BOOK_CHAPTER_LIST = {}

class ChapterTemplate:

    def getChapterList(self,tid):
        bookurl = QDURLConvert().convertBookUrl(tid)
        content = WebPageContent(bookurl)
        feed = BookChapterListParser()
        feed.feed(content.getData())
        result = []
        for item in feed.bookList:
            if len(item.linkUrl)>0:
                result.append(item)

        return result


    def getChapterUrl(self,tid,chapterNum):
        chapterList =self.getChapterList(tid)
        if len(chapterList)>0 and len(chapterList)+1 >= chapterNum:
            return chapterList[chapterNum-1].linkUrl
        return None

    def getChapterDetailByUrl(self,url):
        content = WebPageContent(url)
        parser = BookDetailParser()
        parser.feed(content.getData())

        return parser.content

    def getChapterDetail(self,tid,pid):
        url = QDURLConvert().convertChapterDetailUrl(tid,pid)
        return self.getChapterDetailByUrl(url)



class QDDocumentFetcher(DocumentFetcher):
    def getDocumentPage(self,tid,page=1):
        '''
            获取一个文章页的接口，根据每个站点实现
            返回DocItemDetailPage对象
        '''
        chapter = ChapterTemplate()
        chapterList = chapter.getChapterList(tid)
        # TODO: 获得pid
        # pid =
        content =chapter.getChapterUrl(tid,page)



        # replyItem =  RelyItem(rid,uid,subject,content=content,is_chapter=True)
        # doc=DocItem(tid=tid,
        #             uid=uid,
        #             url=url,
        #             subject=subject,
        #             reply_count=replyCount,
        #             view_count=viewCount,
        #             content=results[0].content,
        #             tags=tags,
        #             fid=fid,
        #             created_at=created_at,
        #             last_reply_at=last_reply_at)
        # return DocItemDetailPage(docItem=doc,page_number=len(chapterList),reply_list[])

    def getLatestDocumentList(self,sid,size):

        listUrl = QDURLConvert().convertBookListUrl(sid,size)
        content = WebPageContent(listUrl)
        parser = BookListByCategoryParser()
        parser.feed(content.getData())
        parser.close()
        bookList = parser.getBookList()
        threadList = []
        cid = QDCategory().getCategoryId(sid)
        for item in bookList:
            tid = re.findall(r'.*/([0-9]+)\.aspx',item.linkUrl)
            subject = item.title
            url = item.linkUrl
            uid = Author().getAuthorByCid(cid)
            docIitem =DocItem(tid=tid,
                              uid=uid,
                              subject=subject,
                              url=url,
                              created_at=item.updateTime,
                              updated_at=item.updateTime
                              )
            threadList.append(docIitem)

        si = SourceInfo(source_id=sid,source_name="",source_desc="",site_id=1)
        return DocumentList(source_info=si,doc_list=threadList)


    def getLatestDocuentList(self,size):
        """
        获得指定站点排行榜的最新文章列表
        """
        pass



if __name__ == "__main__":
    # listUrl = QDURLConvert().convertBookListUrl(1,1)
    # content = WebPageContent(listUrl)
    # parser = BookStoreParser()
    # parser.feed(content.getData())
    # parser.close()
    # bookContent = parser.getBookList()
    # a =u"http://www.qidian.com/Book/2424881.aspx"
    # b = re.findall(r'.*/([0-9]+)\.aspx',a)
    # print(b[0])

    # a =QDDocumentFetcher().getLatestDocumentList(1,1)

    # tmp = ChapterTemplate()
    # a=tmp.getChapterList(2718848)

    content = WebPageContent(u"http://read.qidian.com/BookReader/2718848,45274945.aspx")
    parser = BookDetailParser()
    parser.feed(content.getData())

    print