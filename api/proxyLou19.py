# coding=utf-8
import logging
import sys,os
from httplib2 import Http
import json
import time,re


reload(sys)
sys.setdefaultencoding('utf-8')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myhome.settings")

userName = u"竹影听笛"
uid = 480

from ls.models import Document,Topic,TopicReply

LOU19SITEID=19


class ThreadProxy:

    def getDocumentCharpters(self,siteid,tid,authorUid,begin=1,end=10):
        """
        siteid 站点id
        tid    原站点内容的唯一id
        authorUid ！＝0 的情况：获得该作者的内容（不包括其他用户的评论）
        begin、 end 开始结束章节
        siteid ＋ tid 可以唯一确定一篇小说，根据组合id获得章节内容，如果该内容不存在，需要从原站获取相应的内容并保存下来。
        """
        docCharpter = DocumentCharpter()

        doc = docCharpter.getDocumentBySourceTid(siteid,tid)
        if doc:
            return docCharpter.getCharpters(doc.topic.id,begin,end)
        else:
            thread = Lou19Thread().getThreadInfo(tid,authorUid)
            doc = docCharpter.addThread(thread)

        return docCharpter.getCharpters(doc.topic.id,begin,end)

class DocumentCharpter:

    def getDocumentBySourceTid(self,siteId,tid):
        docs = Document.objects.filter(source_id=siteId).filter(source_tid=tid)
        if len(docs)==0:
            return None
        else:
            return docs[0]


    def addThread(self,thread):

        title = thread["subject"]
        viewCount = thread["viewCount"]
        replyCount = thread["replyCount"]
        categoryid = 104
        content = thread["charpterList"][0]["msg"][0:250]
        fid = thread["fid"]
        tid = thread["tid"]
        topic = Topic(userid=uid,
                      username=userName,
                      title=title,
                      content=content,
                      categoryid=categoryid,
                      catid1=0,
                      catid2=0,
                      read_count=viewCount,
                      reply_count=replyCount,
                      topic_type=Topic.TOPIC_TYPE_DOCUMENT)
        topic.save()
        soureceUrl = "www.19lou.com/forum-"+str(fid)+"-thread-"+str(tid)+"-1-1.html"
        doc=Document(source_id=LOU19SITEID,source_tid=tid,source_url=soureceUrl,topic=topic)
        doc.save()

        postList = thread["charpterList"]
        for item in postList:
            msg = item["msg"]
            title =item["title"]
            pid = item["pid"]
            replyUrl = "www.19lou.com/forum-"+str(fid)+"-thread-"+str(tid)+"-1-1.html"+"#"+str(pid)

            reply = TopicReply(userid=uid,
                               username=userName,
                               topicid=topic.id,
                               title=title,
                               content=msg,
                               is_chapter=True,
                               source_url=replyUrl)
            reply.save()
        return doc


    def getCharpters(self,topicId,begin,end):
        replys = TopicReply.objects.filter(topicid=topicId,is_chapter=True)[begin:end]
        return replys


    def updateDocumentCharpterCount(self,documentId,count):
        pass


class Lou19Thread:

    client_id = 100
    client_secret = u"accessTest7118jqq54113accessTest"
    lou19Url = "https://www.19lou.com/api/thread/getThreadView?client_id=%d&client_secret=%s&filterWater=true"%(client_id,client_secret)
    prePage = 50
    httpHeaders = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}





    def getThreadInfo(self,tid,authorUid=None):
        getAll = False
        pageNum = 1
        postTmp = []
        headers = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
        hClient = Http()
        subject = ""
        viewCount = 0
        replyCount = 0
        fid = 0
        while not getAll:
            try:
                if authorUid==None:
                    threadUrl = self.lou19Url + "&tid=%s"%(str(tid))+"&page="+str(pageNum)+"&perPage="+str(self.prePage)

                else:
                    threadUrl = self.lou19Url + "&tid=%s"%(str(tid))+"&authorUid="+str(authorUid)+"&page="+str(pageNum)+"&perPage="+str(self.prePage)

                resp, content = hClient.request(threadUrl,"GET",headers=headers)
                content = content.decode('gb18030').encode('utf8')
                jsonContent = json.loads(content)
                currentPage = int(jsonContent["page"])
                if len(subject)==0:
                    thread = jsonContent["thread_info"]
                    subject  = thread["subject"]
                    viewCount = int(thread["views"])
                    replyCount = int(thread["replies"])

                if fid==0:
                    forminfo = jsonContent["forum_info"]
                    fid = int(forminfo["fid"])

                if currentPage < pageNum:
                    getAll = True
                else:
                    pageNum += 1

                postList = jsonContent["post_list"]

                if postList:
                    postTmp.append(postList)
                    print 'get page'
                    time.sleep(2)
                    # print threadUrl
                    # print "+++++++++++Size:"+str(len(postList))
                else:
                    getAll = True

            except Exception,e:
                logging.error(e.message)

        result = []
        for item in postTmp:
            for post in item:
                message = self.stripTagsExcludeBr(post["message"])
                title = post["subject"]
                titleString = self.stripTags(message[0:100])
                if len(title)==0:
                    ###获得回复得标题：取100字中，第一个标点符号前面的内容，如果没有直接截取最前的10个字
                    try:
                        tmp = re.split(u'\,|\.|，|。', titleString)[0]
                        if tmp and len(tmp)>0:
                            title = tmp
                        else:
                            title = titleString[0:10]
                    except Exception,e:
                        logging.error(e.message)
                result.append({"msg":message,"pid":post["pid"],"title":title})

        return {"subject":subject,"fid":fid,"tid":tid,"viewCount":viewCount,"replyCount":replyCount,"charpterList":result}


    def stripTags(self,html):
        s = HTMLStripper()
        s.feed(html)
        return s.get_data()

    def stripTagsExcludeBr(self,html):
        s = HTMLStripperExcludeBr()
        s.feed(html)
        return s.get_data()


from HTMLParser import HTMLParser
class HTMLStripper(HTMLParser):
    """
    去除所有得html标签
    """
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)


class HTMLStripperExcludeBr(HTMLParser):
    """
    去除html标签，除了<br>
    """
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)

    def handle_starttag(self, tag, attrs):
        if tag =="br":
            self.fed.append("\\r\\n")

    def get_data(self):
        return ''.join(self.fed)


if __name__ == "__main__":
    pass

    #proxy = ThreadProxy()
    #result = proxy.getDocumentCharpters(19,12011369225965883,31004258,1,10)
    #print
    #for item in result:
        # print "++++++++"
        # print item.title
        # print "======"
        # print item.content

    # <div align="left"><font face="" color="" style="font-size: 18px">&nbsp;&nbsp;&nbsp; 见他还是一副事不关已，只来占便宜的样子，颜千夏便眯眼一笑，小声说道：<BR><br>&nbsp;&nbsp;&nbsp;&nbsp;“现在这药正让我难受，皇上，不如，借你的唇一用？让我泄泄火？”<br><br>&nbsp;&nbsp;&nbsp;&nbsp;“悉听尊便。”<br><br>&nbsp;&nbsp;&nbsp;&nbsp;慕容烈低下头，柔软的唇瓣轻贴在了她的小嘴儿上，颜千夏的眼角荡开几丝得逞的笑意，他还没来得及撤开，颜千夏就已经在他的唇角上狠狠下了口，不客气地留了两枚清晰的牙齿印儿。<br><br>&nbsp;&nbsp;&nbsp;&nbsp;事实告诉他，千万别去欺负一个可怜的小寡妇！<br><br>&nbsp;&nbsp;&nbsp;&nbsp;看着颜千夏在水里快速刨开，慕容烈伸手一抓，便拉住了她的脚踝，她尖叫一声，连连蹬着腿，这药在她血管里正加速运动，让她的尖叫听上去倒像是在求欢的意思。<br><br>&nbsp;&nbsp;&nbsp;&nbsp;“小夏儿，我倒忘了，你一向喜欢咬人的。”<br><br>&nbsp;&nbsp;&nbsp;&nbsp;他俯过身来，把她的腿一下就缠在了自己的腰上，他的某处硬朗就抵在她的腿间。颜千夏猛地瞪大了眼睛，他是来真的，在太皇太后独占的碧莲池里！<br><br>&nbsp;&nbsp;&nbsp;&nbsp;“看来我们得好好谈谈。”<br><br>&nbsp;&nbsp;&nbsp;&nbsp;他高大，水只到他腰上而已，颜千夏的上半身却完全被他托出了水面，胸前的两朵粉莲花颤微微地，让他的声音愈加低哑，他低头就在粉莲上咬了咬，摁着她的腰，就往她的身体里刺去了……<br><br>&nbsp;&nbsp;&nbsp;&nbsp;是，谁也没有想到！<br><br>&nbsp;&nbsp;&nbsp;&nbsp;颜千夏完整得就像一卷刚织好的绵，身体光滑紧窒！他明显地感觉到自己冲破了屏障，他的动作一僵，颜千夏却痛得一声尖叫，手指紧紧地掐进了他的肩膀里。<br><br>&nbsp;&nbsp;&nbsp;&nbsp;该死的，那个夫君居然没和她洞房吗？好歹你也在雕花的婚床上抱着她滚了一晚啊，值更的太监宫女都是这样说的呀，听到洞房里缠绵之声久久不息，帝妃恩爱之情尽在摇曳的龙凤烛之下、大红的龙床之上。<br><br>&nbsp;&nbsp;&nbsp;&nbsp;可是，怎么会这样？<br><br>&nbsp;&nbsp;&nbsp;&nbsp;颜千夏惊骇低头，看着水面上浮起艳红，又被碧水迅速吞噬。<br><br>&nbsp;&nbsp;&nbsp;&nbsp;“慕容烈，你这个……”<br><br>&nbsp;&nbsp;&nbsp;&nbsp;颜千夏欲哭无泪，若早知这样，她一定死守着这身体，以后找个官大业大，或者江湖大侠天下富豪之类的再嫁了，过一段神仙日子才对。现在倒好，糊里糊涂的，倒被他占了便宜去了。<br><br>&nbsp;&nbsp;&nbsp;&nbsp;“真是让朕意外。”<br><br>&nbsp;&nbsp;&nbsp;&nbsp;慕容烈的脸色在短的讶然之后，恢复了平静，摁着她扭动想挣脱的腰，沉声说道：<br><br>&nbsp;&nbsp;&nbsp;&nbsp;“看来，朕得对夏儿温柔一些才对。”<br><br>&nbsp;&nbsp;&nbsp;&nbsp;“滚你的，放开我。”<br><br>&nbsp;&nbsp;&nbsp;&nbsp;颜千夏痛得发抖，挣不脱他的手是小事，关键是这男人一沾了她的身体，那合欢药的威力就跟原子弹似的，在体内炸开了，她再不逃，绝对会反扑过去的！扑谁也不能扑这人啊！<br><br>&nbsp;&nbsp;&nbsp;&nbsp;药性猛得超过颜千夏的估量，合欢散最无情的地方就在于，当事人绝对是清醒的，她清醒地感觉到自己身体的每一寸肌肤都在想往慕容烈身上贴去，体内被点了无数把火，五脏六腑烧得灼烫难忍。<br><br>&nbsp;&nbsp;&nbsp;&nbsp;“算了，你快点，我好难受，太热了。”<br><br>&nbsp;&nbsp;&nbsp;&nbsp;她放弃了挣扎，干脆双手紧搂住了他的脖子，她可不想熬两个时辰，四个小时啊！颜千夏的身子娇贵，据说自小儿就用各色花瓣儿泡过，每日间用数十名奶妈的奶水精心擦拭每一寸肌肤，又服食许多名贵香粉，除了一身异香，还弄得她十分敏感，怕痛怕热怕冷，简直就是个瓷瓶儿，得用双手天天捧着抱着才行。</font></div>
    # """
    # a = HTMLStripperExclude()
    # a.feed(data)
    # print a.get_data()
    # data =" aad，asa,adasaa.adadfas。阿德发发，阿德发发萨。"
    # data = u'要她勾搭小叔子 颜千夏跪了半柱香的时辰了。青色轻纱垂帘，重重叠叠地在风里轻舞，凤栖宫中，森森冷香在殿中萦绕着。金丝帘后坐着一位美艳的妇人，正用长长的指甲挑起一小撮冷香末轻嗅着，满脸陶醉'
    # result =re.split(u'\,|\.|，|。',data)
    # print result