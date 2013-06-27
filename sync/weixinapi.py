# coding=utf-8
from ls.models import Document,Topic,Category
from django.db.models import Q
import re
from datetime import  date,timedelta
import random

REPLY_SUBSCRIBE=u'''欢迎关注精品阅读，每天为您推荐最热门的小说。
另外你还可以按如下六种方式查看推荐内容：
一、按排行榜推荐
    你可以回复“排行榜”，查看近7日小说总排行榜。
二、按小说名查看
    你也可以输入“s+小说标题”查找您想看的小说！如查看《摘星》，回复“S摘星”就能查看。
三、按达人推荐
    您可以回复红太狼‘’CJ的小白‘等获取这些达人推荐的小说。更多达人推荐请回复h查看达人名单。
四、按书评员推荐
    另外您还可以回复‘推荐’，看看苹果米饭等书评员有哪些推荐。
五、按日期查看
    回复“今天”查看今天的推荐内容,要查看往期的推荐可回复日期.如要查看5月19日推荐，回复“519“就行。
六、按门类查看
    您可以回复玄幻、腹黑、重生、耽美、高干等，查看分类的推荐。
'''

REPLY_DEFAULT=u'''
你可按如下六种方式查看推荐内容啦！
一、按排行榜推荐
    你可以回复“排行榜”，查看近7日小说总排行榜。
二、按小说名查看
    你也可以输入“s+小说标题”查找您想看的小说！如查看《摘星》，回复“S摘星”就能查看。
三、按达人推荐
    您可以回复红太狼‘’CJ的小白‘等获取这些达人推荐的小说。更多达人推荐请回复h查看达人名单。
四、按书评员推荐
    另外您还可以回复‘推荐’，看看苹果米饭等书评员有哪些推荐。
五、按日期查看
    回复“今天”查看今天的推荐内容,要查看往期的推荐可回复日期.如要查看5月19日推荐，回复“519“就行。
六、按门类查看
    您可以回复玄幻、腹黑、重生、耽美、高干等，查看分类的推荐。
'''

AUTHORS_LIST=u'''
达人名单：
d1:19楼红太狼
d2:cj的小白
d3:超级懒人一个
d4:nephila
d5:刘美晨子
d6:一眼是你
d7:celinejulie
d8:xp光影
d9:水宽鱼沉
d10:喵了个咪的猫_狸
d11:hhh121
d12:jobowi
d13:忧忧2010
d14:我是果果mami

请回复达人编号或名称获取推荐，多次回复可获取不同推荐。
'''

AUTHORS={u'红太狼':14693355,
         u'19楼红太狼':14693355,
         u'd1':14693355,
         u'cj的小白':22545551,
         u'小白':22545551,
         u'd2':22545551,
         u'超级懒人一个':20152738,
         u'd3':20152738,
         u'nephila':25480616,
         u'd4':25480616,
         u'刘美晨子':27972747,
         u'd5':27972747,
         u'一眼是你':20608805,
         u'd6':20608805,
         u'celinejulie':22710707,
         u'd7':22710707,
         u'xp光影':25092645,
         u'd8':25092645,
         u'水宽鱼沉':28139202,
         u'd9':28139202,
         u'喵了个咪的猫_狸':24183800,
         u'd10':24183800,
         u'hhh121':22775113,
         u'd11':22775113,
         u'jobowi':28103945,
         u'd12':28103945,
         u'忧忧2010':22699953,
         u'd13':22699953,
         u'我是果果mami':27722818,
         u'd14':27722818,
        }


SHUPING=[
    u't1:苹果米饭',
    u't2:初夏蔷薇涩1',
    u't3:下一世的笑颜',
    u't4:樱亡语天使',
    u't5:卞卡123',
    u't6:小西瓜兔兔',
    u't7:luckyheart',
    u't8:堆儿堆儿的',
    u't9:xuweina0512',
    u't10:布丁恋果果',
]
#书评员查询名称与相应的帖子tid对应表
SHUPING_NUM={
    u'苹果米饭':6401363935177114,
    u'米饭':6401363935177114,
    u'苹果':6401363935177114,
    u't1':6401363935177114,
    u'初夏蔷薇涩1':3601363770235717,
    u'初夏蔷薇涩':3601363770235717,
    u't2':3601363770235717,
    u'下一世的笑颜':10001363830631804,
    u't3':10001363830631804,
    u'樱亡语天使':12801363965661378,
    u't4':12801363965661378,
    u'卞卡123':24801363691794516,
    u't5':24801363691794516,
    u'小西瓜兔兔':9501363765496022,
    u't6':9501363765496022,
    u'luckyheart':10101363833819575,
    u't7':10101363833819575,
    u'堆儿堆儿的':22201363832175949,
    u't8':22201363832175949,
    u'xuweina0512':25001364810304166,
    u't9':25001364810304166,
    u'布丁恋果果':8801363774115229,
    u't10':8801363774115229,
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
    msg=msg.lower().strip()
    if u'推荐'==msg:
        txt=u'请回复书评员昵称或编号，看他们的最新推荐：'

        for sname in SHUPING:
            txt=txt+u'\r\n'+sname

        return {'type':'TEXT','text':txt}
    if u'达人'==msg or u'h'==msg:
        return {'type':'TEXT','text':AUTHORS_LIST}
    elif msg==u'排行' or msg==u'排行榜':
        return resp_top(msg)
    elif AUTHORS.has_key(msg):
        return resp_from_author(msg)
    elif SHUPING_NUM.has_key(msg):
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
    return {'type':'TEXT','text':REPLY_DEFAULT}

PATTEN_REPLACE_19URL=re.compile('(?<=http://www.19lou.com/forum-26-thread-)\d+(?=-1-1.html)')
def resp_from_shuping(msg):
    from api.api19 import ThreadApi
    tapi=ThreadApi()
    tp=tapi.getThreadPage(tid=SHUPING_NUM[msg],page=1000) #最后一页
    prevPage=tp.docItem.reply_count/18
    if prevPage<1:
        prevPage=1
    tp0=tapi.getThreadPage(tid=SHUPING_NUM[msg],page=prevPage)
    replys=[]
    di=tp.docItem
    for reply in tp0.reply_list:
        if reply.uid==di.uid and len(reply.content)>100:
            replys.append(reply)
    for reply in tp.reply_list:
        if reply.uid==di.uid and len(reply.content)>100:
            replys.append(reply)

    if len(replys)==0:
        return {'type':'TEXT','text':u'抱歉没有找到合适的推荐，请换个书评员看看吧！'}

    r_num=random.randint(0,len(replys)-1)
    sel_reply=replys[r_num]
    content=sel_reply.content
    while True:
        m=PATTEN_REPLACE_19URL.search(content)
        if m==None:
            break
        tid_19=m.group()
        content=re.sub('http://www.19lou.com/forum-26-thread-%s-1-1.html'%(tid_19),
                       '<a href="http://mobile-proxy.weibols.com/proxy/%s">源文链接☞</a>'%(tid_19),
                       content)
    content=sel_reply.user_name+u'的推荐:\n\r'+content
    content=content+u"\n\r\n\r提示：回复‘s+书名’可以搜索书评中提到的小说。\n\r再次回复编号可以查看该书评员的其它推荐！"
    return {'type':'TEXT','text':content}

def resp_top(msg):
    week=timedelta(days=7)
    today=date.today()
    day_week=today-week
    topics=Topic.objects.filter(status__exact=1).filter(topic_type__exact=2).filter(created_at__gte=day_week).order_by('-read_count')[0:5]
    docs=[]
    for topic in topics:
        if topic.isDocument():
            docs.append(topic.getDocument())
    return {'type':'NEWS','docs':docs}


def resp_from_keyword(msg):
    tagid=TAGS[msg]
    cat = Category.objects.get(pk=tagid)
    topics=Topic.objects.filter(Q(categoryid__exact=tagid)|Q(catid1__exact=tagid)|Q(catid2__exact=tagid)).filter(status__exact=1).filter(topic_type__exact=2).order_by('-created_at')[0:30]

    docs=[]
    for topic in topics:
        if topic.isDocument():
           if len(docs)<=5:
                docs.append(topic.getDocument())
           else:
                s_doc=topic.getDocument()
                docs.append(s_doc)
                for doc in docs:
                    if doc.topic.read_count<s_doc.topic.read_count:
                        s_doc=doc
                docs.remove(s_doc)
           
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

    topics=Topic.objects.filter(status__exact=1).filter(topic_type__exact=2).filter(created_at__gte=day).filter(created_at__lte=day2).order_by('-read_count')[0:5]
    docs=[]

    for topic in topics:
        docs.append(topic.getDocument())

    if len(docs)==0:
        return {'type':'TEXT','text':u'抱歉！没有这一天的内容。如需帮助请回复’h‘或’帮助‘。'}

    return {'type':'NEWS','docs':docs}

def resp_from_author(msg):
    author_uid=AUTHORS[msg]
    count=Document.objects.filter(source_uid__exact=author_uid).count()
    start=random.randint(0,count-10)
    docs=Document.objects.filter(source_uid__exact=author_uid).order_by('-id')[start:start+8]

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