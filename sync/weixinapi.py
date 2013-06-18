# coding=utf-8
from ls.models import Document,Topic,Category
from django.db.models import Q
import re
from datetime import  date,timedelta
REPLY_SUBSCRIBE='''欢迎关注精品阅读，每天为您同步推荐最热门的小说。
回复“今天”查看今天的推荐内容，要查看以前的推荐，可回复日期.如要查看5月19日推荐，回复“519“就可以了。
你也可回复查看言情、玄幻、腹黑、重生、耽美、高干等推荐。你也可以输入【s+空格+小说标题】或【搜+空格+小说标题】查找您想看的小说！'''

AUTHORS={u'红太狼':14693355,
         u'19楼红太狼':14693355,
         u'CJ的小白':22545551,
         u'小白':22545551
}

TAGS={
     u'重生':102,
     u'玄幻':105,
     u'言情':104,
     u'腹黑':115,
     u'高干':137,
     u'耽美':107,
     u'甜宠':112,
     u'穿越':101,
}

RESP_TYPE={'TEXT':1,'NEWS':2}

_RE_SEARCH=re.compile(u'[s|S|搜][ ]+')
def get_response(msg,to):

    if AUTHORS.has_key(msg):
        return resp_from_author(msg)
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
    elif msg==u'昨天':
        day=date.today()-oneday-oneday
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