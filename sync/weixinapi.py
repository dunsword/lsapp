# coding=utf-8
from ls.models import Document,Topic,Category
from django.db.models import Q
import re
from datetime import  date,timedelta
REPLY_SUBSCRIBE='''欢迎关注精品阅读，每天为您推荐最热门的小说。
回复“今天”查看今天的推荐内容.要查看以前的推荐可回复日期.如要查看5月19日推荐，回复“519“就可以了。
你还可回复查看言情、玄幻、腹黑、重生、耽美、高干等分类推荐。你也可以输入【s+小说标题】或【搜+小说标题】查找您想看的小说！
另外，还可以回复’红太狼‘、’CJ的小白‘等获取这些达人推荐的小说。'''

AUTHORS={u'红太狼':14693355,
         u'19楼红太狼':14693355,
         u'CJ的小白':22545551,
         u'小白':22545551,
         u'超级懒人一个':20152738,
         u'nephila':25480616,
         u'刘美晨子':27972747,
         u'一眼是你':20608805,
         u'celinejulie':22710707,
         u'XP光影':25092645,
         u'水宽鱼沉':28139202,
         u'喵了个咪的猫_狸':24183800,
         u'HHH121':22775113,
         u'jobowi':28103945,
         u'忧忧2010':22699953,
         u'我是果果mami':27722818,
        }


SHUPING={
    u'苹果米饭':6401363935177114,
    u'下一世的笑颜':10001363830631804,
}

TAGS={
     u'穿越':101,
     u'重生':102,
     u'都市':103,
     u'言情':104,
     u'玄幻':105,
     u'奇幻':106,
     u'耽美':107,
     u'同人':108,
     u'武侠':109,
     u'仙侠':110,
     u'末世':111,
     u'甜宠':112,
     u'女主':113,
     u'修仙':114,
     u'腹黑':115,
     u'空间':116,
     u'婚后':117,
     u'女强':118,
     u'女尊':119,
     u'现代':120,
     u'师徒':121,
     u'清穿':122,
     u'教授':123,
     u'帝王':124,
     u'架空':125,
     u'姐弟':126,
     u'小白':127,
     u'民国':128,
     u'修真':129,
     u'复仇':130,
     u'宫斗':131,
     u'黑道':132,
     u'总裁':133,
     u'婚恋':134,
     u'豪门':135,
     u'宠文':136,
     u'高干':137,
     u'肉文':138,

}

RESP_TYPE={'TEXT':1,'NEWS':2}

_RE_SEARCH=re.compile(u'[s|S|搜][+]*[ ]*')
def get_response(msg,to):

    if AUTHORS.has_key(msg):
        return resp_from_author(msg)
    elif SHUPING.has_key(msg):
        return resp_from_shuping(msg)
    elif  TAGS.has_key(msg):
        return resp_from_keyword(msg)
    elif _RE_SEARCH.match(msg)!=None:
       g= _RE_SEARCH.match(msg)
       return search(msg[len(g.group(0)):])
    else:
        result=get_date(msg)
        if result!=None:
            return result
    return {'type':'TEXT','text':REPLY_SUBSCRIBE}

def resp_from_shuping(msg):
    from api.api19 import ThreadApi
    tapi=ThreadApi()
    tp=tapi.getThreadPage(tid=SHUPING[msg],page=1000) #最后一页
    replys=[]
    di=tp.docItem
    for reply in tp.reply_list:
        if reply.uid==di.uid:
            replys.append(reply)


def resp_from_keyword(msg):
    tagid=TAGS[msg]
    cat = Category.objects.get(pk=tagid)
    topics=Topic.objects.filter(Q(categoryid__exact=tagid)|Q(catid1__exact=tagid)|Q(catid2__exact=tagid)).filter(status__exact=1).filter(topic_type__exact=2).order_by('-created_at')[0:5]
    docs=[]
    for topic in topics:
        if topic.isDocument():
           docs.append(topic.getDocument())

    result=u""
    num=1

    return {'type':'NEWS','docs':docs}
    # for doc in docs:
    #     result=result+str(num)+u'、'+doc.topic.title+u': http://121.199.9.13/proxy/'+str(doc.source_tid)+u'\r\n'
    #     num=num+1
    # return result


_DATE_RE=re.compile('[\d]{3,4}$')
def get_date(msg):
    oneday=timedelta(days=1)

    if msg==u'今天':
        day=date.today()-oneday #时间为昨天，避免没有内容
        day2=day+oneday+oneday
    elif msg==u'昨天':
        day=date.today()-oneday-oneday
        day2=day+oneday
    else:
        g=_DATE_RE.match(msg)
        if g==None:
            return None

        num=int(msg)
        daynum=num%100
        month=num/100
        try:
            day=date(2013,month,daynum)
        except:
            return {'type':'TEXT','text':u'请输入正确的日期如：601。如需帮助请回复’h‘或’帮助‘。'}
        day2=day+oneday

    topics=Topic.objects.filter(status__exact=1).filter(topic_type__exact=2).filter(created_at__gte=day).filter(created_at__lte=day2).order_by('-created_at')[0:5]
    docs=[]

    for topic in topics:
        docs.append(topic.getDocument())

    if len(docs)==0:
        return {'type':'TEXT','text':u'抱歉！没有这一天的内容。如需帮助请回复’h‘或’帮助‘。'}

    return {'type':'NEWS','docs':docs}

def resp_from_author(msg):
    author_uid=AUTHORS[msg]
    docs=Document.objects.filter(source_uid__exact=author_uid).order_by('-id')[0:8]

    if len(docs)==0:
        return {'type':'TEXT','text':u'抱歉！没有找到合适的内容。如需帮助请回复’h‘或’帮助‘。'}
    return {'type':'NEWS','docs':docs}

def search(keyword):
    topics=Topic.objects.filter(title__contains=keyword).filter(topic_type__exact=2)[0:8]
    docs=[]
    for topic in topics:
        docs.append(topic.getDocument())
    if len(docs)==0:
        return {'type':'TEXT','text':u'抱歉！没有找到合适的内容。如需帮助请回复’h‘或’帮助‘。'}
    return {'type':'NEWS','docs':docs}

if __name__=='__main__':
    resp=get_response('腹黑')
    print resp