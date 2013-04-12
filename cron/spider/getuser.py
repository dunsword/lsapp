# coding=utf-8

import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")

import urllib
from sgmllib import SGMLParser

password = u"password"

class Pinyin(object):
    """translate chinese hanzi to pinyin by python, inspired by flyerhzm’s
    `chinese\_pinyin`_ gem

    usage
    -----
    ::
        In [1]: from xpinyin import Pinyin
        In [2]: p = Pinyin()
        In [3]: p.get_pinyin(u"上海")
        Out[3]: 'shanghai'
        In [4]: p.get_initials(u"上")
        Out[4]: 'S'
    请输入utf8编码汉字
    .. _chinese\_pinyin: https://github.com/flyerhzm/chinese_pinyin
    """

    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'Mandarin.dat')

    def __init__(self):
        self.dict = {}
        for line in open(self.data_path):
            k, v = line.split('\t')
            self.dict[k] = v

    def get_pinyin(self, chars=u'你好', splitter=''):
        result = []
        for char in chars:
            key = "%X" % ord(char)
            try:
                result.append(self.dict[key].split(" ")[0].strip()[:-1]
                .lower())
            except:
                result.append(char)
        return splitter.join(result)

    def get_initials(self, char=u'你'):
        try:
            return self.dict["%X" % ord(char)].split(" ")[0][0]
        except:
            return char



class WebPageContent:
    """ 根据url获得页面的内容用于数据分析 """
    def __init__(self,url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()
    def getData(self):
        return self.htmlSource

class SpiderUser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.avatarurl = u""
        self.username = u""
        self.email = u""
        self.photoDiv = False
        self.userInfo = False

    def handle_data(self, text):
        pass


    def start_div(self,attrs):
        userPhoto = [v for k, v in attrs if k == 'class' and v == 'big-photo']
        if userPhoto:
            self.photoDiv = True


    def end_div(self):
        if self.photoDiv:
            self.photoDiv = False


    def start_img(self,attrs):
        if self.photoDiv:
            self.avatarurl = [v for k, v in attrs if k == 'src'][0]
            self.username = [v for k, v in attrs if k == 'alt'][0]
            self.email = Pinyin().get_pinyin(self.username) + "@tuitui.com"


    def end_img(self):
        pass


if __name__ == "__main__":
    # url = "http://file2.qidian.com/face/6/51/651029100x100.png"
    # urllib.urlretrieve(url,r"/Users/yanggz/myPythonSpace/1.jpg")
    #print Pinyin().get_pinyin("中国")

    from base.models import User
    #beginId = 20396
    beginId = 3211000
    i = 0
    while i<500:
        i += 1
        id  =beginId+i
        content = WebPageContent("http://me.qdmm.com/authorIndex.aspx?id=%s"%(id))
        parser = SpiderUser()
        parser.feed(content.getData())
        parser.close()
        userName = parser.username
        if len(userName.strip("\r\n").strip())>0:
            user = User.objects.create_user(parser.username, parser.email, password,parser.username)
            # 另存图片
            avatarUrl = parser.avatarurl.strip("\r\n").strip()
            if len(avatarUrl)>0:
                try:
                    urllib.urlretrieve(avatarUrl,r"/Users/yanggz/myPythonSpace/djangoPrj/lsapp/static/avatar/a_250X250_%s.jpg"%(str(user.id)))
                except:
                    if avatarUrl.startswith("/Images/"):
                        avatarUrl = "http://me.qdmm.com" + avatarUrl
                        urllib.urlretrieve(avatarUrl,r"/Users/yanggz/myPythonSpace/djangoPrj/lsapp/static/avatar/a_250X250_%s.jpg"%(str(user.id)))

