# coding=utf-8
__author__ = 'XPS'
from django.views.generic.base import View
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ls.models import Document,Category,Topic,TopicReply
from ls.topic_forms import TopicForm,TopicReplyForm,TopicService,TopicReplyService,DocumentForm
from ls.document_forms import DocumentService
from django.utils.decorators import method_decorator
from base.base_view import BaseView, PageInfo
from ls.views import LsView
from api.huatan import Huatan
from sync.models import source_author
from django.db.models import Q

_HUATAN_API=Huatan()
class TuijianViews(LsView):
    def get(self,request, source_uid,version='',page=1,*args, **kwargs):
        '''

        :param request:
        :param source_uid:
        :param version:
        :param page:
        :param args:
        :param kwargs:
        '''
        if request.GET.__contains__('page'):
            page=int(request.GET['page'])
        else:
            page=1
        try:
            author=source_author.objects.get(Q(uid__exact=source_uid)&Q(site_id__exact=19))
            userName=author.username
        except source_author.DoesNotExist:
            userName=_HUATAN_API.getUserName(source_uid)
            author=source_author(uid=source_uid,username=userName,desc=u'',site_id=19)
            author.save()


        count=Document.objects.filter(source_uid__exact=source_uid).count()
        pageInfo=PageInfo(page,count,10,'/m/daren/'+str(source_uid)+'?page=')
        docs=Document.objects.filter(source_uid__exact=source_uid).filter(topic__status__exact=1).order_by('-topic__created_at')[pageInfo.startNum:pageInfo.endNum]
        c = self.getContext(request,
                            {
                             'user_name':userName,
                             'desc':author.desc,
                             'pageinfo':pageInfo,
                             'source_uid':source_uid,
                             'docs':docs,
                             })

        tt = loader.get_template(version+'ls_daren.html')
        return HttpResponse(tt.render(c))
