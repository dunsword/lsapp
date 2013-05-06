# Create your views here.
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from base.models import User
from ls.models import Topic, TopicManager
from datetime import datetime


@csrf_exempt
def create_topic(request):
    data = {}
    userId = request.POST['user_id']
    topicTitle = request.POST['topic_title']
    topicContent = request.POST['topic_content']
    catId = request.POST['cat_id']
    topicType = request.POST['topic_type']
    user = User.objects.get(pk=userId)
    # 如果用户不存在，则返回对应的错误
    if not user:
        data['result'] = False
        data['message'] = 'user not exist!'
        return HttpResponse(data, content_type='application/json')

    # 验证标题名称，如果没有，暂时先返回
    if not topicTitle:
        data['result'] = False
        data['message'] = 'topic title need!'
        return HttpResponse(data, content_type='application/json')

    # 验证内容，如果没有，暂时先返回
    if not topicContent:
        data['result'] = False
        data['message'] = 'topic content need!'
        return HttpResponse(data, content_type='application/json')
    topic_type = Topic.TOPIC_TYPE_NORMAL
    if topicType == Topic.TOPIC_TYPE_DOCUMENT or topicType == Topic.TOPIC_TYPE_VIDEO or topicType == Topic.TOPIC_TYPE_SHOP:
        topic_type = topicType

    # 验证内容，如果没有，暂时先返回
    if not catId:
        data['result'] = False
        data['message'] = 'topic category id need!'
        return HttpResponse(data, content_type='application/json')

    topic = Topic(userid=user.id,
                  username=user.username,
                  title=topicTitle,
                  content=topicContent,
                  categoryid=catId,
                  created_at=datetime.now(),
                  updated_at=datetime.now(),
                  topic_type=topic_type)

    topic.save()

    if topic.id:
        data['result'] = True
    else:
        data['result'] = False
    return HttpResponse(data, content_type='application/json')