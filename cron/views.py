# coding=utf-8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ls.models import Document,Topic
from cron.models import DocumentMapping,CategoryAuthor
from datetime import datetime
import random
from django.utils import simplejson as json


"""
        内容相关数据结构的定义：
        2.回复
            发帖人，章节名称、章节内容、章节更新时间、章节url地址、章节唯一的id
        {'uid':122,
         'userName':"",
         'title':"",
         'content':"",
         'date':"",
         'refUrl':"",
         'refId':122
        }

        3.评论
            评论人、评论时间、评论内容

"""

@csrf_exempt
def newDocument(request):
    """
    1.主贴：
        发帖人、标题、内容简介、发帖时间、所属分类id、来源站点id，来源站点小说的唯一id,小说原站url
        {'datas':[
            {'uid':122,
             'userName':"",
             'title':u"aaa",
             'content':"",
             'date':"",
             'cid':111,
             'refSiteId':1,
             'refId':1223,
             'refUrl':"",
             'wordnum',5678,
             'readnum':123,
             'author':''
            }
        ]
        }
    :param request:
    :return:
    """
    error = []
    result = []

    for item in json.loads(request.body).get("datas"):
        try:
            uid = item.get("uid", 0)
            userName = item.get("userName", "")
            title = item.get("title", "")
            content = item.get("content", "")
            date = item.get("date", "")
            cid = item.get("cid", 0)
            refSiteId = item.get("refSiteId", 0)
            refId = item.get("refId", 0)
            refUrl = item.get("refUrl", "")
            wordnum = item.get('wordnum',0)
            readnum = item.get('readnum',0)
            author = item.get('author','')
            if  len(title.strip())>0 and  len(content.strip())>0:
                if readnum ==0:
                    readnum = random.randint(1000, 5000)
                try:
                    dt = datetime.strptime(date, "%Y-%m-%d %H:%M")
                except Exception,e:
                    print e
                    dt = datetime.now()

                # 只完成新增数据
                topic=Topic(userid=uid,
                            username=userName,
                            title=title,
                            content=content,
                            categoryid=cid,
                            catid1=0,
                            catid2=0,
                            updated_at=dt,
                            created_at=dt,
                            read_count=readnum,
                            topic_type=Topic.TOPIC_TYPE_DOCUMENT)
                topic.save()

                doc=Document(source_id=refSiteId,
                             source_url=refUrl,
                             topic=topic,
                             word_count=wordnum,
                             author_name=author,
                             source_updated_at=dt)
                doc.save()

                result.append({'docId':doc.id,'refid':refId})

        except Exception, e:
            print e
            error.append({'errormsg':e.message,'refId':refId})

    return HttpResponse(json.dumps({'message':'data saved', 'errormsg':error, 'result': result}), content_type='application/json')



@csrf_exempt
def updateDocument(request):
    """
    1.主贴：
        发帖人、标题、内容简介、发帖时间、所属分类id、来源站点id，来源站点小说的唯一id,小说原站url
        {'datas':[
        {'docId':122,
         'refId':12345,
         'readnum':333,
         'wordnum',5678,
         'date':""
        }]
        }
    :param request:
    :return:
    """
    error = []
    for item in json.loads(request.body).get("datas"):
        try:
            docId = item.get("docId", 0)
            refId = item.get("refId", 0)
            readnum = item.get("readnum", 0)
            wordnum = item.get("wordnum", 0)
            date = item.get("date", "")
            if not docId==0:
                if readnum ==0:
                    readnum = random.randint(1000, 10000)
                try:
                    dt = datetime.strptime(date, "%Y-%m-%d %H:%M")
                except:
                    dt = datetime.now()
                #更新数据
                doc = Document.objects.filter(id=docId).update(word_count=wordnum)
                Topic.objects.filter(id=doc.topic.id).update(read_count=readnum,updated_at=dt)
        except Exception, e:
            print e
            error.append({'errormsg':e.message,'refId':refId})

    return HttpResponse(json.dumps({'message':'data updated', 'errormsg':error, 'result': 'Ok'}), content_type='application/json')

