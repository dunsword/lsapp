# coding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
from sgmllib import SGMLParser

USERID = 1

USERLIST = ['/p/头发乱了xxoo']

class WebPageContent:
    """ 根据url获得页面的内容用于数据分析 """
    def __init__(self,url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()
    def getData(self):
        return self.htmlSource


class UserAvatar(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.avartarDiv = False
        self.avartarUrl = u''
        self.otherUsrs = []

    def handle_data(self, text):
        pass


    def start_div(self,attrs):
        avatarDiv = [v for k, v in attrs if k == 'class' and v == 'user-portrait']
        if avatarDiv:
            self.avartarDiv = True


    def end_div(self):
        if self.avartarDiv:
            self.avartarDiv = False

    def start_a(self,attrs):
        if self.avartarDiv:
            isUserName = [v for k, v in attrs if k == 'class' and v == 'user-online']
            if isUserName:
                userName = [v for k, v in attrs if k == 'href'][0]
                USERLIST.append(userName)
                print userName

    def end_a(self):
        pass


    def start_img(self,attrs):
        global USERID
        if self.avartarDiv:
            avartarUrl = [v for k, v in attrs if k == 'src'][0]
            avartarUrl = avartarUrl.replace('portraitn','portrait')
            urllib.urlretrieve(avartarUrl,r"/Users/yanggz/myPythonSpace/djangoPrj/lsapp/static/a_250X250_%s.jpg"%(str(USERID)))
            USERID += 1
            print  avartarUrl


    def end_img(self):
        pass

class DataProcess():
    def getUserKey(self,userName):
        url = "http://www.baidu.com"+userName
        content = WebPageContent(url)
        resultContent = content.getData()
        num1 = resultContent.find("'portrait' :")
        num2 = resultContent.find("'sexTitle' :")
        userKey = resultContent[num1+13:num2].strip("\r\n").strip().replace("'",'').replace(',','')
        return userKey

    def getUserLists(self,userKey):
        url = "http://www.baidu.com/p/sys/data/tieba/userlist?portrait="+userKey+"&part=follow"
        content = WebPageContent(url)
        resultContent = content.getData()
        num =resultContent.find("\"tplContent\":")
        parser = UserAvatar()
        parser.feed(resultContent[num+14:len(resultContent)-5].replace('\/',"/").replace('\\x22',"'"))
        parser.close()


if __name__ == "__main__":

    for item in USERLIST:
        print item
        dateProcess = DataProcess()
        userKey = dateProcess.getUserKey(item)
        dateProcess.getUserLists(userKey)
        USERLIST.remove(item)

    print

    # content = WebPageContent("http://www.baidu.com/p/是烟不是火")
    # # # content = WebPageContent("http://www.baidu.com/p/sys/data/tieba/userlist?rec=1000026&portrait=1398e5a4b4e58f91e4b9b1e4ba8678786f6f8a2f&part=follow&t=1368604627944")
    # # # content = WebPageContent("http://www.baidu.com/p/sys/data/tieba/userlist?rec=1000026&part=follow")
    # resultContent = content.getData()
    #
    # print resultContent
    # #
    # num1=resultContent.find("'portrait' :")
    # num2=resultContent.find("'sexTitle' :")
    # #
    # userKey =resultContent[num1+13:num2].strip("\r\n").strip().replace("'",'').replace(',','')
    # url ="http://www.baidu.com/p/sys/data/tieba/userlist?portrait="+userKey+"&part=follow"
    # #
    # print url
    #
    # num =resultContent.find("\"tplContent\":")
    # # result = resultContent[num+14:len(resultContent)-5]
    # # print result
    # # a = result.replace('\/',"/")
    # #
    # # print a
    # #
    # # b = a.replace('\\x22',"'")
    # #
    # # t = b.find('\\x22')
    # #
    # # print b
    #
    #
    # parser = UserAvatar()
    # parser.feed(resultContent[num+14:len(resultContent)-5].replace('\/',"/").replace('\\x22',"'"))
    # parser.close()
