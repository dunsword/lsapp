# coding=utf-8
import sys
import os
import re
import urllib
import threading
import random
from sgmllib import SGMLParser
from httplib2 import Http
from django.utils import simplejson as json

reload(sys)
sys.setdefaultencoding('utf-8')
type = sys.getfilesystemencoding()

'''
功能：目前采用抓取分类，然后按照分类进行抓取3页，然后对每页的每个链接抓取对应的信息
运行：直接运行文件，Spider类进行多线程分发，按照每个分类，进行不同的页面抓取（这里分类采用七点的大分类）
      Timer是根据不同的分类进行调用RecursionPage抓取页面包
全局参数说明：
      localDomain：远程需要调用写入接口的域名
      categoryDict：红袖和本地的对应关系，有些起点有的本地没有，暂时不调用
      userMap：用户字典，形式为cid对应一个用户list
      dirFileName：hongxiu的日志，说明跑过那些东西，下次跑的时候只需要修改就行了
'''


#全局变量
localDomain = u'http://127.0.0.1:8000'
#全局文件日志
dirFileName = u"hongxiuspider.log"

#全局变量
# localDomain = u'http://weibols.sinaapp.com'
#全局文件日志
# dirFileName = u"hongxiuspider.log"


#分类的对应，前面是起点的categoryId，后面对应接口的categoryId
categoryDict = {
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

userMap = {101: [{"name": "九城烟岚", "uid": 731}, {"name": "人品棣", "uid": 485}, {"name": "便便羊", "uid": 354},
                 {"name": "向阳光处飞", "uid": 37}, {"name": "夜隐默", "uid": 301}, {"name": "失魂崖", "uid": 769},
                 {"name": "斗鱼1992", "uid": 42}],
           102: [{"name": "俺不在家", "uid": 136}, {"name": "吹风的好日子", "uid": 185}, {"name": "小小珠子", "uid": 540},
                 {"name": "小酒浅酌丨", "uid": 454}, {"name": "影火舞", "uid": 463}, {"name": "文子敬手", "uid": 514}],
           103: [{"name": "ADYS", "uid": 272}, {"name": "zhao家2少", "uid": 645}, {"name": "一花开百花败", "uid": 75},
                 {"name": "亲吻鱼的尾巴", "uid": 373}, {"name": "伧瑾小空空", "uid": 371}, {"name": "冬雪收藏", "uid": 748},
                 {"name": "北木北", "uid": 180}, {"name": "十三寸", "uid": 640}, {"name": "卖萌屌丝猫", "uid": 231},
                 {"name": "南宫天伦1990", "uid": 215}, {"name": "双生暗影", "uid": 452}, {"name": "名字好难起12", "uid": 297},
                 {"name": "听海抱月", "uid": 263}, {"name": "唯陶渊明之独爱菊", "uid": 309}, {"name": "大道掌控者", "uid": 72},
                 {"name": "小通灵", "uid": 362}, {"name": "忘尘雨露", "uid": 460}, {"name": "才不是秀吉", "uid": 46},
                 {"name": "无情无念", "uid": 605}, {"name": "无语之家", "uid": 529}],
           104: [{"name": "い普罗旺斯的薰衣草未开つ", "uid": 506}, {"name": "亭阁一介", "uid": 603}, {"name": "但纷纷如皋人", "uid": 713},
                 {"name": "僵尸是丧失", "uid": 74}, {"name": "古月孤云", "uid": 601}],
           105: [{"name": "72男孩", "uid": 16}, {"name": "Chaoˉ逆〃鳞", "uid": 294}, {"name": "Godmiracle", "uid": 762},
                 {"name": "beluuu", "uid": 752}, {"name": "刘星羽", "uid": 222}, {"name": "司空神威Z", "uid": 628},
                 {"name": "唱八绝", "uid": 481}, {"name": "坐望风雷", "uid": 382}, {"name": "小豆爱素", "uid": 517},
                 {"name": "无叹息", "uid": 282}, {"name": "无啊吖", "uid": 33}],
           106: [{"name": "伍易", "uid": 636}, {"name": "夙清云", "uid": 712}, {"name": "大脚黄连香", "uid": 209},
                 {"name": "宇暖心", "uid": 672}, {"name": "惘月翼", "uid": 343}],
           107: [{"name": "Play223", "uid": 457}, {"name": "msleel", "uid": 138}, {"name": "·小盛", "uid": 573},
                 {"name": "『墨雪殇』醉", "uid": 462}, {"name": "万年烟丝", "uid": 259}, {"name": "佤柳", "uid": 281},
                 {"name": "依冷如此", "uid": 734}, {"name": "十三豆12", "uid": 234}, {"name": "咆哮草履虫", "uid": 108},
                 {"name": "啦啦喔类", "uid": 41}, {"name": "回首看日落", "uid": 350}, {"name": "复仇苍狼", "uid": 770},
                 {"name": "左岸anger", "uid": 369}, {"name": "旎红鱼", "uid": 753}],
           108: [{"name": "Chrisviel", "uid": 89}, {"name": "不爱不傻", "uid": 736}, {"name": "久美紫", "uid": 701},
                 {"name": "修翎晨夢", "uid": 655}, {"name": "千殇控丶", "uid": 199}, {"name": "天铭男神", "uid": 203},
                 {"name": "奋斗小辉", "uid": 183}, {"name": "小小骚男", "uid": 740}, {"name": "小白逛逛", "uid": 166},
                 {"name": "斯年惟静", "uid": 755}, {"name": "无端弄弦", "uid": 364}, {"name": "星璇月&泠", "uid": 230}],
           109: [{"name": "三十谢", "uid": 276}, {"name": "上官信", "uid": 83}, {"name": "与君休", "uid": 320},
                 {"name": "伽蓝寺的烟花", "uid": 329}, {"name": "冬瓜南瓜西瓜", "uid": 227}, {"name": "四暗杠", "uid": 385},
                 {"name": "地瓜莲藕", "uid": 312}, {"name": "大汉英灵", "uid": 404}, {"name": "天剑帝王", "uid": 683},
                 {"name": "太上花开", "uid": 541}, {"name": "头大的成群", "uid": 768}, {"name": "幽火魂", "uid": 147},
                 {"name": "影火燎天", "uid": 468}, {"name": "我名为佐", "uid": 87}],
           110: [{"name": "HOLD蝴蝶", "uid": 625}, {"name": "Y逍遥公子J", "uid": 300}, {"name": "伟琐", "uid": 561},
                 {"name": "南小莫", "uid": 232}, {"name": "可爱的小贱男", "uid": 450}, {"name": "四V空间", "uid": 388},
                 {"name": "寡人老诗", "uid": 306}, {"name": "微品鹧鸪", "uid": 547}, {"name": "念素娥", "uid": 357},
                 {"name": "无心思念", "uid": 334}],
           111: [{"name": "TDY爽哥", "uid": 696}, {"name": "″烟毒", "uid": 190}, {"name": "依山涟水", "uid": 193},
                 {"name": "冷幻の冰凝", "uid": 687}, {"name": "夜掌孤灯", "uid": 582}, {"name": "孤孤单单不寂寞", "uid": 122},
                 {"name": "小浩子的故事", "uid": 556}, {"name": "尹娜娜yin", "uid": 24}],
           112: [{"name": "2哒叶", "uid": 650}, {"name": "SKasun", "uid": 322}, {"name": "天晴一度", "uid": 326},
                 {"name": "恰巧遇到你", "uid": 391}, {"name": "昔年的阳光", "uid": 318}, {"name": "是非不是", "uid": 482}],
           113: [{"name": "Mysterian", "uid": 352}, {"name": "云不颠", "uid": 544}, {"name": "伊家伊", "uid": 501},
                 {"name": "冷眼830", "uid": 221}, {"name": "听骂", "uid": 47}, {"name": "城中烟雨", "uid": 291},
                 {"name": "天炫风云", "uid": 212}, {"name": "安言若梦", "uid": 296}, {"name": "思闲云", "uid": 7}],
           114: [{"name": "bns剑灵控", "uid": 118}, {"name": "丿早已疲惫丨", "uid": 515}, {"name": "再见北极星", "uid": 188},
                 {"name": "半缕凉烟", "uid": 175}, {"name": "回家的外星人", "uid": 654}, {"name": "圣休", "uid": 592},
                 {"name": "天涯忆柔", "uid": 759}, {"name": "奕飞冲天", "uid": 749}, {"name": "子成成", "uid": 135}],
           115: [{"name": "4季", "uid": 210}, {"name": "99大叔", "uid": 707}, {"name": "b白日做梦", "uid": 347},
                 {"name": "tutu13", "uid": 351}, {"name": "不屈之圣", "uid": 649}, {"name": "兮琉年", "uid": 336},
                 {"name": "刀々客", "uid": 747}, {"name": "剑刀笑♀", "uid": 240}, {"name": "唐门染月", "uid": 549},
                 {"name": "奔尘", "uid": 577}, {"name": "文中皇", "uid": 295}],
           116: [{"name": "一盅天", "uid": 102}, {"name": "事事惔惔", "uid": 588}, {"name": "半夜听雨芭蕉", "uid": 679},
                 {"name": "布叶猴", "uid": 165}, {"name": "弑神十三", "uid": 114}, {"name": "懒么么", "uid": 244},
                 {"name": "护念", "uid": 685}],
           117: [{"name": "AP猫帝", "uid": 729}, {"name": "一样的吧", "uid": 728}, {"name": "公子劫", "uid": 652},
                 {"name": "化折天", "uid": 307}, {"name": "喜欢乐C", "uid": 742}, {"name": "山水妮子", "uid": 546}],
           118: [{"name": "buke110", "uid": 186}, {"name": "三百万大军", "uid": 358}, {"name": "也没化工厂v", "uid": 95},
                 {"name": "寒小米", "uid": 607}, {"name": "小女淡然", "uid": 671}, {"name": "崖山醉人", "uid": 527},
                 {"name": "忘岛", "uid": 585}, {"name": "无敌王少", "uid": 73}],
           119: [{"name": "三秦刀客", "uid": 21}, {"name": "东王一小博", "uid": 176}, {"name": "古月映残阳", "uid": 31},
                 {"name": "啊凡伟", "uid": 487}, {"name": "富翁九州", "uid": 735}, {"name": "尘羽君", "uid": 590},
                 {"name": "恶心的胖子", "uid": 648}, {"name": "我不相信天", "uid": 132}, {"name": "打酱油的油瓶", "uid": 55},
                 {"name": "推猜未来", "uid": 160}],
           120: [{"name": "不计回报", "uid": 107}, {"name": "叶蘖少爷", "uid": 96}, {"name": "天狼星岛", "uid": 252},
                 {"name": "抬头便是云朵", "uid": 551}, {"name": "旷野中的吼叫", "uid": 9}],
           121: [{"name": "LF路漫漫", "uid": 524}, {"name": "SATAN冰", "uid": 65}, {"name": "caocaodewu", "uid": 402},
                 {"name": "l龙霸", "uid": 49}, {"name": "七魄书生", "uid": 461}, {"name": "兔子帮帮帮", "uid": 699},
                 {"name": "半薇一下", "uid": 726}, {"name": "土包子大村姑", "uid": 261}, {"name": "墨夜临晗", "uid": 530},
                 {"name": "尚在人世", "uid": 314}, {"name": "愚昧连胜", "uid": 758}, {"name": "明月孤鸿", "uid": 664}],
           122: [{"name": "云若心想", "uid": 659}, {"name": "亮123玲", "uid": 224}, {"name": "天天小天天", "uid": 8},
                 {"name": "孤阴孤阳", "uid": 552}, {"name": "徐佐819301963", "uid": 613}, {"name": "无良之宅男", "uid": 635}],
           123: [{"name": "丁瑜AD", "uid": 616}, {"name": "三流散人", "uid": 507}, {"name": "不乐山水", "uid": 84},
                 {"name": "全能钙片", "uid": 365}, {"name": "凤箫言尘", "uid": 182}, {"name": "午夜歌殇", "uid": 151},
                 {"name": "哈哈忙呀哈哈", "uid": 611}, {"name": "我是青橄榄", "uid": 375}, {"name": "戥辰", "uid": 127},
                 {"name": "施拉姆", "uid": 398}, {"name": "无罪天团", "uid": 439}, {"name": "晓初无名", "uid": 218}],
           124: [{"name": "=坂上智代=", "uid": 268}, {"name": "hi大尾巴狼", "uid": 597}, {"name": "东方夏天", "uid": 703},
                 {"name": "偷吃番茄酱的猫", "uid": 464}, {"name": "千儿万女", "uid": 290}, {"name": "叔神不二", "uid": 198},
                 {"name": "唐小水", "uid": 621}, {"name": "尘焰雪", "uid": 330}, {"name": "布衣氏族", "uid": 279},
                 {"name": "斯蒂芬李斯克", "uid": 366}, {"name": "星辰绝恋熏儿", "uid": 275}, {"name": "星辰龙珧", "uid": 714}],
           125: [{"name": "临安初雨时", "uid": 355}, {"name": "伪心的物语", "uid": 283}, {"name": "冰灵舞帝", "uid": 598},
                 {"name": "妖冶de丶邪魅", "uid": 760}, {"name": "孤辰星风", "uid": 739}, {"name": "我妹万岁", "uid": 615},
                 {"name": "戚魇翎の森林", "uid": 377}],
           126: [{"name": "C妏雯", "uid": 443}, {"name": "再徐徐图之", "uid": 340}, {"name": "冥寂之吻", "uid": 109},
                 {"name": "喷火的蜗牛", "uid": 662}, {"name": "小小彡柒", "uid": 723}, {"name": "影火天袭", "uid": 455}],
           127: [{"name": "2013陌弃", "uid": 323}, {"name": "事实上我21", "uid": 325}, {"name": "伍玉林", "uid": 181},
                 {"name": "勉强幸福123", "uid": 171}, {"name": "华夏メ魂", "uid": 642}, {"name": "悄悄等待", "uid": 416}],
           128: [{"name": "baby莹莹", "uid": 406}, {"name": "·情殇", "uid": 724}, {"name": "一颗孤寂的草", "uid": 97},
                 {"name": "亲吻礼", "uid": 548}, {"name": "写手无情", "uid": 446}, {"name": "天蓝Rekly", "uid": 667},
                 {"name": "天龙苍", "uid": 571}, {"name": "安洛七", "uid": 237}, {"name": "小晴川", "uid": 163},
                 {"name": "岚夜笙歌", "uid": 271}, {"name": "我我我啊哎", "uid": 56}],
           129: [{"name": "X残剑破", "uid": 247}, {"name": "孙剑飞恩恩", "uid": 521}, {"name": "御龙三世", "uid": 417}],
           130: [{"name": "FH书友", "uid": 214}, {"name": "Pal5", "uid": 315}, {"name": "T2病毒", "uid": 81},
                 {"name": "不破的阵眼", "uid": 643}, {"name": "君无遗", "uid": 545}, {"name": "咖啡泡大蒜", "uid": 61},
                 {"name": "囧囧猪小帅", "uid": 374}, {"name": "帝尊一统", "uid": 152}, {"name": "广大一写手啊", "uid": 368},
                 {"name": "怒笑横刀", "uid": 153}, {"name": "我挖坑你来跳", "uid": 390}, {"name": "我是李冬晨", "uid": 379},
                 {"name": "断剑的书生", "uid": 286}, {"name": "星孤子", "uid": 442}],
           131: [{"name": "何为人是为忍", "uid": 70}, {"name": "千山雪寂", "uid": 653}, {"name": "宇桦的", "uid": 270}],
           132: [{"name": "Konight", "uid": 410}, {"name": "一缕红尘&泪", "uid": 15}, {"name": "七宗罪之", "uid": 591},
                 {"name": "丶烟灭", "uid": 229}, {"name": "什么什么洋芋片", "uid": 39}, {"name": "叶凡初", "uid": 678},
                 {"name": "天上的云彩儿", "uid": 618}, {"name": "天洐", "uid": 475}, {"name": "小明童鞋live", "uid": 18},
                 {"name": "尹金金", "uid": 200}],
           133: [{"name": "____江南", "uid": 562}, {"name": "听雨滴花开", "uid": 310}, {"name": "墨千越", "uid": 513}],
           134: [{"name": "JACKW", "uid": 543}, {"name": "T木易T", "uid": 531}, {"name": "一坛小菜", "uid": 201},
                 {"name": "余定和", "uid": 299}, {"name": "凛冬·", "uid": 437}, {"name": "坑爹d", "uid": 761},
                 {"name": "太叔皓", "uid": 100}, {"name": "孤单空城", "uid": 641}, {"name": "寒血伤", "uid": 82},
                 {"name": "师弟陆大友", "uid": 156}, {"name": "御妖圣者", "uid": 274}],
           135: [{"name": "Only灬小艺", "uid": 429}, {"name": "Silence灵魂", "uid": 167}, {"name": "Tariq", "uid": 604},
                 {"name": "夜来疯语", "uid": 535}, {"name": "少年未少年", "uid": 504}, {"name": "心不想不念", "uid": 421},
                 {"name": "斜阳霓虹", "uid": 256}, {"name": "无忧阿莫凡", "uid": 140}],
           136: [{"name": "DaveWong", "uid": 40}, {"name": "mayyico", "uid": 409}, {"name": "skyyl2010", "uid": 342},
                 {"name": "亦我非我", "uid": 349}, {"name": "孤雨寂云", "uid": 17}, {"name": "摩根席尔瓦", "uid": 356}]}#下一页的url

# 文件的临时内存存放地点，这个不需要修改
fileContent = u""


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
        # 这个是当需要借口调用的时候，采用这个方法实现
        # if not userMap.get(cid):
        #     url = u"%s/cron/getAuthors?cid=%d" % (localDomain, cid)
        #     userCategoryList = []
        #     h = Http()
        #     resp, content = h.request(url, "GET")
        #     for item in json.loads(content).get("datas"):
        #         user = User(int(item.get("uid")), item.get("name"))
        #         userCategoryList.append(user)
        #     if userCategoryList:
        #         print 'this is init time'
        #         userMap[cid] = userCategoryList
        #     else:
        #         return User(2, u'user1')
        userList = userMap.get(cid)
        userDict = random.choice(userList)
        return User(userDict['uid'], userDict['name'])

    def postContent(self, uid, userName, title, content, date, cid, refSiteId, refId, refUrl, wordnum, readnum, author):
        params = json.dumps({'datas': [
            {'uid': uid, 'userName': userName, 'title': title,
             'content': content, 'date': date,
             'cid': cid, 'refSiteId': refSiteId, 'refId': refId, 'refUrl': refUrl,
             'wordnum': wordnum, 'readnum': readnum, 'author': author}
        ]})
        headers = {"Content-type": "application/json", "Accept": "text/plain", "User-Agent": "Magic Browser"}
        h = Http()
        url = u"%s/cron/add" % localDomain
        resp, content = h.request(url, "POST", body=params, headers=headers)
        docId = 0
        if json.loads(content).get("errormsg"):
            print json.loads(content).get("errormsg")
            return docId
        for item in json.loads(content).get("result"):
            docId = int(item.get("docId"))
        return docId

    def updateContent(self, docId, refId, readnum, wordnum, date):
        try:
            params = json.dumps({'datas': [
                {'docId': docId, 'refId': refId, 'readnum': readnum,
                 'wordnum': wordnum, 'date': date}
            ]})
            headers = {"Content-type": "application/json", "Accept": "text/plain", "User-Agent": "Magic Browser"}
            h = Http()
            url = u"%s/cron/update" % localDomain
            resp, content = h.request(url, "POST", body=params, headers=headers)
            if json.loads(content).get("errormsg"):
                print json.loads(content).get("errormsg")
                return 0
            return 1
        except Exception, e:
            print e
            pass
        return 0


class BookAccessLog:
    def open(self, fileName=dirFileName):
        if not os.path.isfile(dirFileName):
            temp = open(dirFileName, 'w')
            temp.close()
        global fileContent
        if not fileContent:
            file_object = open(fileName)
            try:
                fileContent = file_object.read()
            finally:
                file_object.close()

    def write(self, fileName=dirFileName):
        global fileContent
        if fileContent:
            file_object = open(fileName, 'w')
            try:
                file_object.write(fileContent)
            finally:
                file_object.close()
                fileContent = u""


class BookStoreData:
    def __init__(self):
        self.title = u''
        self.linkUrl = u''
        self.author = u''
        self.updateTime = u''
        self.wordNum = 0
        self.readNum = 0
        self.lastPostTitle = u''
        self.lastPostUrl = u''


class BookStoreParser(SGMLParser):
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

    def end_dt(self):
        if self.isLastPost:
            self.isLastPost = False

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


class UTF8Parser(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.hasMatch = False
        self.readNum = 0
        self.wordNum = 0
        self.isScript = 0
        self.hasScript = False

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


class BookInfoParser(SGMLParser):
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


class RecursionPage:
    def __init__(self, url, cid=0, startPage=1, totalPage=10):
        self.cid = cid
        self.url = url
        self.start = startPage
        self.end = totalPage
        self.run()

    def run(self):
        content = WebPageContent(self.url)
        pattern = re.compile(r'http://.*?/')
        fidPattern = re.compile(r'http://.*?/[a-zA-Z0-9]/([0-9]+)/')
        parser = BookStoreParser()
        parser.feed(content.getData().decode('gbk').encode('utf-8'))
        parser.close()
        bookContent = parser.getBookList()

        if bookContent:
            global fileContent
            logFile = BookAccessLog()
            logFile.open()
            for item in bookContent:
                url = item.linkUrl
                lMatch = pattern.match(url)
                if not lMatch:
                    url = u'http://novel.hongxiu.com/' + item.linkUrl
                m = fidPattern.match(url)
                fid = 0
                if m:
                    fid = int(m.group(1))
                fidAccessPattern = re.compile(".*?\[%d,([0-9]+)\].*?" % fid)
                fa = fidAccessPattern.match(fileContent)
                pid = 0
                if fa:
                    pid = int(fa.group(1))
                bi = BookInfo(url, self.cid, fid=fid, item=item)
                # bi = BookInfo(u'http://novel.hongxiu.com/a/643818/"', self.cid, fid=fid, item=item)
                res = bi.run(pid)
                if res > 0:
                    fileContent += u"[%d,%d]" % (fid, res)
            logFile.write()

            if self.start < self.end:
                if parser.nextUrl:
                    nextUrl = parser.nextUrl
                    nm = pattern.match(nextUrl)
                    if not nm:
                        nextUrl = u'http://www.hongxiu.com' + nextUrl
                    RecursionPage(nextUrl, self.cid, self.start + 1, self.end)
                    # else:
                    #     thread.exit_thread()


class BookInfo:
    def __init__(self, url, cid=0, fid=0, item=None):
        self.cid = cid
        self.url = url
        self.fid = fid
        self.book = item

    def setUp(self):
        if not self.fid:
            pattern = re.compile(r'http://.*?/[a-zA-Z0-9]/([0-9]+)/')
            m = pattern.match(self.url)
            if m:
                self.fid = int(m.group(1))

    def run(self, pid=0):
        self.setUp()
        content = WebPageContent(self.url)
        utf8Parser = UTF8Parser()
        utf8Parser.feed(content.getData())
        parser = BookInfoParser()
        if utf8Parser.hasMatch:
            parser.feed(content.getData())
        else:
            parser.feed(content.getData().decode('gb2312', 'ignore').encode('utf-8'))

        parser.close()
        hm = HttpMonitor()
        user = hm.user(self.cid)
        if user:
            if pid > 0:
                hm.updateContent(pid, self.fid, utf8Parser.readNum, utf8Parser.wordNum, self.book.updateTime)
                print u'pid[%d], fid[%d] is update success; word count is [%s]; read number is [%s]; update time is [%s];' % (
                pid, self.fid, utf8Parser.wordNum, utf8Parser.readNum, self.book.updateTime)
                print self.url
            else:
                resPid = hm.postContent(user.uid, user.name, self.book.title, parser.intro,
                                        self.book.updateTime, self.cid, 2, self.fid, self.url, utf8Parser.wordNum,
                                        utf8Parser.readNum,
                                        self.book.author)
                # resPid = 1
                print u'pid[%d], fid[%d] is add success; word count is [%d]; read number is [%d]; create time is [%s];' % (
                resPid, self.fid, utf8Parser.wordNum, utf8Parser.readNum, self.book.updateTime)
                return resPid
        return 0


class Timer(threading.Thread):
    def __init__(self, url, cid):
        threading.Thread.__init__(self)
        self.url = url
        self.cid = cid
        self.thread_stop = False

    def run(self):
        RecursionPage(self.url, self.cid)


class Spider():
    def __init__(self):
        self.run()

    def run(self):
        for key in categoryDict:
            url = u'http://www.hongxiu.com/novel/s/%s_1_order9.html' % key
            RecursionPage(url, categoryDict[key])

            # 如果不是多线程，按照上面来，如果是多线程，则按照下面来，
            # 下面开启后，需要在RecursionPage中开启thread.exit_thread()
            # thread = Timer(url, categoryDict[key])
            # thread.start()


if __name__ == "__main__":
    print 'hongxiu spider is runing'
    Spider()
    print 'hongxiu spider is end'