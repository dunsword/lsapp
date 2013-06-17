# coding=utf-8
from ls.models import Document,Topic,Category
from django.db.models import Q

REPLY_SUBSCRIBE='''欢迎关注精品阅读，每天为您同步推荐最热门的小说。
回复“今天”查看今天的推荐内容，要查看一月内任一天的推荐，可回复日期.
如要查看5月19日推荐，回复“519“就可以了。你也可回复查看言情、玄幻、腹黑、重生、耽美、高干等推荐。'''

AUTHORS={'红太郎':14693355,
         '19楼红太郎':14693355,
         'CJ的小白':22545551,
         '小白':22545551
}

TAGS={
     u'重生':102,
     u'玄幻':105,
     u'言情':104,
     u'腹黑':115,
     u'高干':137,
     u'耽美':107,
     u'甜宠':112,
}

RESP_TYPE={'TEXT':1,'NEWS':2}

def get_response(msg,to):
    if AUTHORS.has_key(msg):
        return resp_from_author(msg)
    elif  TAGS.has_key(msg):
        return resp_from_keyword(msg)
    else:
        return REPLY_SUBSCRIBE

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



def resp_from_author(msg):
    return "author"+msg


if __name__=='__main__':
    resp=get_response('腹黑')
    print resp