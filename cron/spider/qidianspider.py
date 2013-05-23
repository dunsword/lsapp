# coding=utf-8
import logging
import os
import sys
import re
import urllib
import random
import StringIO
import sqlite3
from sgmllib import SGMLParser
from httplib2 import Http
from django.utils import simplejson as json

reload(sys)
sys.setdefaultencoding('utf-8')

'''
功能：目前采用抓取分类，然后按照分类进行抓取3页，然后对每页的每个链接抓取对应的信息
运行：直接运行文件，Spider类进行多线程分发，按照每个分类，进行不同的页面抓取（这里分类采用七点的大分类）
      Timer是根据不同的分类进行调用RecursionPage抓取页面包
全局参数说明：
      localDomain：远程需要调用写入接口的域名
      categoryDict：起点和本地的对应关系，有些起点有的本地没有，暂时不调用
      userMap：用户字典，形式为cid对应一个用户list
      dirFileName：七点的日志，说明跑过那些东西，下次跑的时候只需要修改就行了
'''

#全局变量
localDomain = u'http://127.0.0.1:8000'

#全局变量
# localDomain = u'http://weibols.sinaapp.com'

jumpFlagFile = u'qidianjump'

logger = logging.getLogger()
logFile = logging.FileHandler("qd_spider.error.log")
logger.addHandler(logFile)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
logFile.setFormatter(formatter)
logger.setLevel(logging.INFO)

#分类的对应，前面是起点的categoryId，后面对应接口的categoryId
categoryDict = {
    '1': 106, # 奇幻
    '21': 105, # 玄幻
    # '2': 109, # 武侠
    # '22': 110, # 仙侠
    # '4': 103, # 都市
    # '15': 104, # 青春 这个暂时先对应 言情
    # #'5': xxx, # 历史 这个没法对应
    # '6': 120, # 军事  这个暂时先对应 现代
    # #'7': '', # 游戏
    # #'8': '', # 竞技
    # '9': 105, # 科幻
    # #'10': '', # 灵异
    # '12': 108, # 同人
    # #'14': '', # 图文
    # #'31': '', # 文学
    # #'41': '', # 女生
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
                 {"name": "亦我非我", "uid": 349}, {"name": "孤雨寂云", "uid": 17}, {"name": "摩根席尔瓦", "uid": 356}]}


class SpiderLog:
    def __init__(self, fid=0, lastPid=0, lsPid=0, link=u'', updateTime=u'', readNum=0, wordNum=0, listUrl=u''):
        self.fid = fid
        self.lastPid = lastPid
        self.lsPid = lsPid
        self.link = link
        self.updateTime = updateTime
        self.readNum = readNum
        self.wordNum = wordNum
        self.listUrl = listUrl


'''
120万的数据，写入文件大概20s
操作100万的数据，内存时间大概45s
120万的数据，从文件读取到内存大概19s
'''


class DBManage:
    def __init__(self):
        # 表名
        self.tableName = u'qd_spider_log'
        # 内存数据库
        self.dbName = u':memory:'
        self.db = sqlite3.connect(self.dbName)
        # 文件数据库
        self.fileDBName = u'qd_spider_log.db'
        self.fileDB = sqlite3.connect(self.fileDBName)

    def insert(self, log=SpiderLog()):
        if not log.fid:
            return False
        cu = self.db.cursor()
        sql = u"insert into %s values(%d, %d, %d, '%s', '%s', %d, %d, '%s')" % (
            self.tableName, log.fid, log.lastPid, log.lsPid, log.link, log.updateTime,
            log.readNum, log.wordNum, log.listUrl)
        cu.execute(sql)
        self.db.commit()
        cu.close()
        return True

    def select(self, fid):
        cu = self.db.cursor()
        sql = u"select * from %s where fid = %d limit 1" % (self.tableName, fid)
        cu.execute(sql)
        result = cu.fetchone()
        cu.close()
        return result

    def truncateDBTable(self):
        cu = self.db.cursor()
        sql = u"delete from %s" % self.tableName
        cu.execute(sql)
        self.db.commit()
        cu.close()

    def truncateFileDBTable(self):
        cu = self.fileDB.cursor()
        sql = u"delete from %s" % self.tableName
        cu.execute(sql)
        self.fileDB.commit()
        cu.close()

    def delete(self, fid):
        if not fid:
            return False
        cu = self.db.cursor()
        sql = u"delete from %s where fid = %d" % (self.tableName, fid)
        cu.execute(sql)
        self.db.commit()
        cu.close()
        return True

    def update(self, fid, lastPid=0, readNum=0, updateTime=u'', wordNum=0, lsPid=0):
        if not fid:
            return False
        if not lastPid and not readNum and not updateTime and not wordNum:
            return False
        sql = u"update %s set " % self.tableName
        if lastPid:
            sql += u"last_pid = %d," % lastPid
        if readNum:
            sql += u"read_num = %d," % readNum
        if updateTime:
            sql += u"update_time = '%s'," % updateTime
        if wordNum:
            sql += u"word_num = '%d'," % wordNum
        if lastPid:
            sql += u"ls_pid = %d," % lsPid
        sql = sql[0:len(sql) - 1] + u" where fid = %d" % fid
        cu = self.db.cursor()
        cu.execute(sql)
        self.db.commit()
        cu.close()
        return True

    def close(self):
        self.db.close()
        self.fileDB.close()

    def copyToFile(self):
        str_buffer = StringIO.StringIO()
        for line in self.db.iterdump():
            str_buffer.write('%s\n' % line)
        self.db.close()
        cur_file = self.fileDB.cursor()
        try:
            cur_file.execute(u"drop table %s" % self.tableName)
        except sqlite3.OperationalError:
            pass
        cur_file.executescript(str_buffer.getvalue())
        cur_file.close()

    def copyToMemory(self):
        str_buffer = StringIO.StringIO()
        for line in self.fileDB.iterdump():
            str_buffer.write('%s\n' % line)
        cur_file = self.db.cursor()
        try:
            cur_file.execute(u"drop table %s" % self.tableName)
        except sqlite3.OperationalError:
            pass
        try:
            cur_file.executescript(str_buffer.getvalue())
            cur_file.execute(u"select * from %s limit 1" % self.tableName)
        except sqlite3.OperationalError:
            # 如果这里是测试，则不需要退出，如果不是测试，则需要退出
            # 第一次跑的时候，需要注释，生成db表
            # exit()
            sql = u"""create table %s (
            fid integer primary key,
            last_pid integer,
            ls_pid integer,
            link varchar(100),
            update_time varchar(20),
            read_num integer,
            word_num integer,
            list_url varchar(200)
            )""" % self.tableName
            cur_file.execute(sql)
            self.db.commit()
        cur_file.close()


class SpiderContent:
    def __init__(self, fid=0, wordNum=0, readNum=0, updateTime=u'', uid=0, name=u'', title=u'', intro=u'', cid=0,
                 url=u'', author=u'', isAdd=0, lsPid=0):
        self.isAdd = isAdd
        self.randomNum = random.randint(1, 10000)
        self.fid = fid
        self.readNum = readNum
        self.wordNum = wordNum
        self.updateTime = updateTime
        self.lsPid = lsPid
        self.uid = uid
        self.name = name
        self.title = title
        self.intro = intro
        self.cid = cid
        self.url = url
        self.author = author


class ContentDBManage:
    def __init__(self):
        # 表名
        self.tableName = u'qd_spider_content'
        # 内存数据库
        self.dbName = u':memory:'
        self.db = sqlite3.connect(self.dbName)

    def reset(self):
        cu = self.db.cursor()
        try:
            cu.execute(u"drop table %s" % self.tableName)
        except sqlite3.OperationalError:
            pass
        finally:
            sql = u"""create table %s (
            is_add integer,
            fid integer,
            word_num integer,
            read_num integer,
            update_time varchar(20),
            ls_pid integer,
            title varchar(1000),
            intro text,
            cid integer,
            url varchar(100),
            author varchar(100),
            random_num integer
            )""" % self.tableName
            cu.execute(sql)
            self.db.commit()
        cu.close()

    def select(self):
        cu = self.db.cursor()
        sql = u'select * from %s order by random_num' % self.tableName
        cu.execute(sql)
        result = cu.fetchall()
        cu.close()
        return result

    def insert(self, content=SpiderContent()):
        if not content.fid:
            return False
        cu = self.db.cursor()
        sql = u"insert into %s values(%d, %d, %d, %d, '%s', %d, '%s', '%s', %d, '%s', '%s', %d)" % (
            self.tableName, content.isAdd, content.fid, content.wordNum, content.readNum, content.updateTime,
            content.lsPid, content.title, content.intro, content.cid, content.url,
            content.author, content.randomNum)
        cu.execute(sql)
        self.db.commit()
        cu.close()
        return True

    def close(self):
        self.db.close()

    def truncate(self):
        try:
            cu = self.db.cursor()
            sql = u"delete from %s" % self.tableName
            cu.execute(sql)
            self.db.commit()
            cu.close()
        except sqlite3.OperationalError:
            pass

    def execute(self):
        result = self.select()
        db = DBManage()
        hm = HttpMonitor()
        if result:
            for content in result:
                isAdd = content[0]
                fid = content[1]
                wordNum = content[2]
                readNum = content[3]
                updateTime = content[4]
                #如果是新增的则调用新增接口，否则调用更新接口
                if isAdd == 1:
                    title = content[6]
                    intro = content[7]
                    cid = content[8]
                    url = content[9]
                    author = content[10]
                    user = hm.user(cid)
                    resPid = hm.postContent(user.uid, user.name, title, intro, updateTime, cid, 1, fid, url, wordNum,
                                            readNum, author)
                    print u"content add success"
                    if resPid > 0:
                        db.update(fid, lsPid=resPid)
                else:
                    pid = content[5]
                    hm.updateContent(pid, fid, readNum, wordNum, updateTime)
                    print u"content update success"
        self.truncate()


class BookList:
    def __init__(self, fid=0, pid=0, title=u"", linkUrl=u"", isVip=0):
        self.fid = fid
        self.pid = pid
        self.title = title
        self.linkUrl = linkUrl
        self.isVip = isVip


class BookListManage:
    def __init__(self):
        # 表名
        self.tableName = u'qd_spider_list'
        self.tableDetailName = u"qd_spider_detail"
        # 内存数据库
        self.dbName = u':memory:'
        self.db = sqlite3.connect(self.dbName)
        # 文件数据库
        self.fileDBName = u'qd_spider_list.db'
        self.fileDB = sqlite3.connect(self.fileDBName)

    def reset(self):
        cu = self.db.cursor()
        sql = u"""create table %s (
            fid integer,
            pid integer,
            title varchar(100),
            link_url varchar(100),
            is_vip integer(1)
            )""" % self.tableName
        cu.execute(sql)
        self.db.commit()
        cu.close()

        fcu = self.fileDB.cursor()
        try:
            fcu.execute(u"select * from %s limit 1" % self.tableDetailName)
        except sqlite3.OperationalError:
            sql = u"""create table %s (
            fid integer,
            pid integer,
            title varchar(200),
            link varchar(100),
            content text,
            update_time varchar(20)
            )""" % self.tableDetailName
            fcu.execute(sql)
            self.fileDB.commit()
        fcu.close()

    def insert(self, chapter=BookList()):
        cu = self.db.cursor()
        sql = u"insert into %s values(%d, %d, '%s', '%s', %d)" % (
            self.tableName, chapter.fid, chapter.pid, chapter.title, chapter.linkUrl, chapter.isVip)
        cu.execute(sql)
        self.db.commit()
        cu.close()
        return True

    def select(self, fid, pid):
        cu = self.db.cursor()
        sql = u"select * from %s where fid=%d and pid=%d limit 1" % (self.tableName, fid, pid)
        cu.execute(sql)
        result = cu.fetchone()
        if result:
            return True
        else:
            return False


    def insertDetail(self, fid, pid, title, linkUrl, content, updateTime):
        cu = self.fileDB.cursor()
        sql = u"insert into %s values(%d, %d, '%s', '%s', '%s', '%s')" % (
            self.tableDetailName, fid, pid, title, linkUrl, content, updateTime)
        cu.execute(sql)
        self.fileDB.commit()
        cu.close()
        return True

    def truncate(self):
        cu = self.db.cursor()
        sql = u"delete from %s" % self.tableName
        cu.execute(sql)
        self.db.commit()
        cu.close()

    def close(self):
        self.db.close()
        self.fileDB.close()

    def copyToFile(self):
        cu = self.db.cursor()
        fcu = self.fileDB.cursor()
        dataSql = u"select * from %s " % self.tableName
        dataResult = cu.execute(dataSql)
        if dataResult:
            try:
                fcu.execute(u"select * from %s limit 1" % self.tableName)
            except sqlite3.OperationalError:
                sql = u"""create table %s (
                    fid integer,
                    pid integer,
                    title varchar(100),
                    link_url varchar(100),
                    is_vip integer(1)
                    )""" % self.tableName
                fcu.execute(sql)
                self.fileDB.commit()
                pass
            result = cu.fetchall()
            fcu.executemany(u"insert into %s values (?,?,?,?,?)" % self.tableName, result)
        fcu.close()
        cu.close()
        self.fileDB.commit()


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


class BookListData:
    def __init__(self):
        self.title = u""
        self.linkUrl = u""


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


class BookStoreParser(SGMLParser):
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
        self.totalClick = u''
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
        self.isTotalClick = False
        self.isTotalClickContentDiv = False
        self.isTotalClickIntro = False
        self.isTotalClickTBody = False
        self.isTotalClickTR = False
        self.isTotalClickTD = False
        self.isTotalClickB = False
        #update tag
        self.isUpdateTime = False
        self.isUpdateTimeDiv = False
        #remove tag
        self.isNotProcess = False
        self.introDeep = 0

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
        if self.isTotalClickTD and not self.isTotalClickB:
            self.totalClick += text.strip("\r\n").strip(u"　").strip()

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

            if not self.totalClick:
                dataDiv = [v for k, v in attrs if k == 'id' and v == 'contentdiv']
                if dataDiv:
                    self.isTotalClickContentDiv = True
                if self.isTotalClickContentDiv:
                    dataIntro = [v for k, v in attrs if k == 'class' and v == 'intro']
                    if dataIntro:
                        self.isTotalClickIntro = True
                if self.isTotalClickIntro:
                    dataLi = [v for k, v in attrs if k == 'class' and v == 'data']
                    if dataLi:
                        self.isTotalClick = True

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
                if self.isIntro:
                    introNotProcess = [v for k, v in attrs if k == 'id' and v == 'ctl00_MainZonePart_pnlVoteActivity']
                    if introNotProcess:
                        self.introDeep = 3
                        self.isNotProcess = True

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
        if self.isIntro and self.deep == self.deepIntro and self.introDeep == 0:
            self.isIntro = False
            self.deep -= 1
            # this is for book info end
            self.deep -= 1
        if self.isIntro and self.introDeep == 0:
            self.isNotProcess = False
        if self.isIntro and self.introDeep > 0:
            self.introDeep -= 1
        if self.isLastVipPostTitle and self.deep == self.deepLastPostTitle:
            self.isLastVipPostTitle = False
            self.deep -= 1
            # if self.isTotalClick:
            #     self.isTotalClick = False

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
        if self.isTotalClickTD:
            self.isTotalClickB = True

    def end_b(self):
        if self.isIntro and self.isNotProcess:
            self.isNotProcess = False
        if self.isTotalClickB:
            self.isTotalClickB = False

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

    def start_table(self, attrs):
        if self.isTotalClick:
            self.isTotalClickTBody = True

    def end_table(self):
        if self.isTotalClickTBody:
            self.isTotalClickTBody = False

    def start_tr(self, attrs):
        if self.isTotalClickTBody:
            self.isTotalClickTR = True

    def end_tr(self):
        if self.isTotalClickTR:
            self.isTotalClickTR = False

    def start_td(self, attrs):
        if self.isTotalClickTR:
            self.isTotalClickTD = True

    def end_td(self):
        if self.isTotalClickTD:
            self.isTotalClickTD = False
            self.isTotalClickTR = False
            self.isTotalClickTBody = False
            self.isTotalClick = False
            self.isTotalClickContentDiv = False
            self.isTotalClickIntro = False


class BookListParser(SGMLParser):
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


class BookListInfo:
    def __init__(self, db, cdb, ldb, url, fid):
        self.db = db
        self.cdb = cdb
        self.ldb = ldb
        self.url = url
        self.fid = fid
        self.domain = u'http://read.qidian.com'
        self.pidPattern = re.compile(r'http://.*?/([a-zA-Z0-9,]+),([0-9]+)\.aspx')
        self.run()

    def run(self):
        content = WebPageContent(self.url)
        pattern = re.compile(r'http://.*?/')
        parser = BookListParser()
        try:
            parser.feed(content.getData())
        except Exception, e:
            print e
        parser.close()
        listContent = parser.getTitleList()
        fidResult = self.db.select(self.fid)
        if listContent:
            for item in listContent:
                if item.linkUrl and item.title:
                    lMatch = pattern.match(item.linkUrl)
                    isVip = True
                    if not lMatch:
                        item.linkUrl = self.domain + item.linkUrl
                        isVip = False
                    m = self.pidPattern.match(item.linkUrl)
                    pid = 0
                    if m:
                        pid = int(m.group(2))
                    lastPid = 0
                    if fidResult:
                        lastPid = fidResult[1]
                    if not self.ldb.select(self.fid, pid) and pid > lastPid:
                        #TODO 这里需要发送到接口，需要在insert之前发送
                        self.ldb.insert(
                            BookList(fid=self.fid, pid=pid, title=item.title, linkUrl=item.linkUrl, isVip=int(isVip)))
                        self.db.update(fid=self.fid, lastPid=pid)
                        print self.fid, pid
                        if not isVip:
                            BookDetail(self.ldb, self.fid, pid, item.title, item.linkUrl)


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
                        self.content = c.getData().decode('GB2312', 'ignore').encode('utf-8').strip(u"document.write('"). \
                            strip(u"<a href=http://www.qidian.com>起点中文网 www.qidian.com 欢迎广大书友光临阅读，"
                                  u"最新、最快、最火的连载作品尽在起点原创！</a>');").strip().replace(u'　', u'');
                except IndexError:
                    pass


class BookDetail:
    def __init__(self, ldb, fid, pid, title, url):
        self.ldb = ldb
        self.url = url
        self.fid = fid
        self.pid = pid
        self.title = title
        self.run()

    def run(self):
        content = WebPageContent(self.url)
        parser = BookDetailParser()
        parser.feed(content.getData())
        parser.close()
        self.ldb.insertDetail(self.fid, self.pid, self.title, self.url, parser.content, parser.updateTime)


class RecursionPage:
    def __init__(self, url, db, cdb, ldb, cid=0, startPage=1, totalPage=1):
        self.cid = cid
        self.url = url
        self.db = db
        self.cdb = cdb
        self.ldb = ldb
        self.start = startPage
        self.end = totalPage
        self.run()

    def run(self):
        content = WebPageContent(self.url)
        pattern = re.compile(r'http://.*?/')
        fidPattern = re.compile(r'http://.*?/([0-9]+)\.aspx')
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
                    url = parser.bookBaseUrl + item.linkUrl
                m = fidPattern.match(url)
                if m:
                    fid = int(m.group(1))
                else:
                    continue
                try:
                    BookInfo(url, self.db, self.cdb, self.ldb, self.cid, fid=fid, totalCount=item.totalCount)
                    # BookInfo(u"http://www.qidian.com/Book/2767774.aspx", self.db, self.cdb, self.ldb, self.cid, fid=2767774, totalCount=item.totalCount)
                except Exception, e:
                    logger.error(str(e))

            if self.start < self.end:
                if parser.nextUrl:
                    RecursionPage(parser.nextUrl, self.db, self.cdb, self.ldb, self.cid, self.start + 1, self.end)
                    # thread.exit_thread()


class BookInfo:
    def __init__(self, url, db, cdb, ldb, cid=0, fid=0, totalCount=0):
        self.cid = cid
        self.url = url
        self.db = db
        self.cdb = cdb
        self.ldb = ldb
        self.fid = fid
        self.totalCount = totalCount
        self.listUrl = u''
        self.run()

    def setUp(self):
        if os.path.exists(jumpFlagFile):
            self.cdb.execute()
            self.db.copyToFile()
            exit()
        if not self.fid:
            pattern = re.compile(r'http://.*?/([0-9]+)\.aspx')
            m = pattern.match(self.url)
            if m:
                self.fid = int(m.group(1))
        self.listUrl = u'http://read.qidian.com/BookReader/%d.aspx' % self.fid

    def run(self):
        self.setUp()
        content = WebPageContent(self.url)
        parser = BookInfoParser()
        parser.feed(content.getData())
        parser.close()
        book = self.db.select(self.fid)
        if book:
            wordNum = book[6]
            if wordNum < self.totalCount:
                self.cdb.insert(SpiderContent(fid=self.fid, wordNum=self.totalCount, readNum=int(parser.totalClick),
                                              updateTime=parser.updateTime, lsPid=book[2]))
                print u"insert into content db for update"
                BookListInfo(self.db, self.cdb, self.ldb, self.listUrl, self.fid)
        else:
            self.cdb.insert(SpiderContent(fid=self.fid, wordNum=self.totalCount, readNum=int(parser.totalClick),
                                          updateTime=parser.updateTime, title=parser.title, intro=parser.intro,
                                          cid=self.cid, url=self.url, author=parser.author, isAdd=1))
            print u"insert into content db for insert"
            BookListInfo(self.db, self.cdb, self.ldb, self.listUrl, self.fid)


class Spider():
    def __init__(self):
        self.run()

    def run(self):
        db = DBManage()
        db.copyToMemory()
        cdb = ContentDBManage()
        cdb.reset()
        ldb = BookListManage()
        ldb.reset()
        for key in categoryDict:
            url = u'http://all.qidian.com/Book/BookStore.aspx?ChannelId=%s' % key
            RecursionPage(url, db, cdb, ldb, categoryDict[key])
        cdb.execute()
        db.copyToFile()


if __name__ == "__main__":
    print 'qidian spider is runing'
    Spider()
    print 'qidian spider is end'