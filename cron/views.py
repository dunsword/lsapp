# coding=utf-8

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from ls.models import Document,Topic
from cron.models import DocumentMapping
from datetime import datetime
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
        {'uid':122,
         'userName':"",
         'title':u"aaa",
         'content':"",
         'date':"",
         'cid':111,
         'refSiteId':1,
         'refId':1223,
         'refUrl':""
        }
    :param request:
    :return:
    """
    error =[]

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

            try:
                dt = datetime.strptime(date, "%Y-%m-%d %H:%M")
            except:
                dt = datetime.now()

            # 先根据站点id和内容id验证是否已经存在。如果存在，只需要更新时间，如果不存在完成新增操作。
            docObj = DocumentMapping.objects.get(source_id=refSiteId,source_document_id=refId)
            if docObj:
                try:
                    topic = Document.objects.get(id=docObj.document_id).topic
                    Topic.objects.filter(id=topic.id).update(updated_at=dt)
                except Exception,e2:
                    print e2.message
                    document = Document.objects.create_document(userid=uid,
                                                                username=userName,
                                                                title=title,
                                                                content=content,
                                                                source_id=refSiteId,
                                                                source_url=refUrl,
                                                                categoryid=cid,
                                                                source_updated_at=dt
                                                                )
                    Topic.objects.filter(id=document.topic.id).update(updated_at=dt,created_at=dt)
            else:
                document = Document.objects.create_document(userid=uid,
                                                            username=userName,
                                                            title=title,
                                                            content=content,
                                                            source_id=refSiteId,
                                                            source_url=refUrl,
                                                            categoryid=cid,
                                                            source_updated_at=dt
                                                            )
                Topic.objects.filter(id=document.topic.id).update(updated_at=dt,created_at=dt)

                # 保存来源数据到数据同步表中
                docMapping = DocumentMapping(document_id=document.id, source_document_id=refId, source_id=refSiteId)
                docMapping.save()
        except Exception, e:
            print e
            error.append({'errormsg':e.message,'refId':refId})

    return HttpResponse({'message':'data saved', 'errormsg':error, 'result': True}, content_type='application/json')
