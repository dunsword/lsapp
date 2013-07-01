#coding=utf-8


from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from base.base_view import  BaseView
from converter import DocumentConvert
from ls.models import Document,TopicReply
from datetime import datetime
from base.base_view import PageInfo
from sync.models import source_author
from sync.author_forms import AuthorForm

class AuthorListView(BaseView):
    def get(self,request,page,*args, **kwargs):
        user=request.user
        if not user.is_staff:
            return self._get_json_respones({'result':'error'})

        page=int(page)
        count=source_author.objects.all().count()
        pageInfo = PageInfo(page=page,itemCount=count,pageSize=20,baseUrl=u'/sync/authors/')
        authors=source_author.objects.all()[pageInfo.startNum:pageInfo.endNum]
        c = RequestContext(request,
                            {
                                'authors':authors,
                                'pageInfo':pageInfo,
                             })

        tt = loader.get_template('sync_authors.html')
        return HttpResponse(tt.render(c))

class AuthorEditView(BaseView):
    def get(self,request,uid,*args,**kwargs):
        user=request.user
        if not user.is_staff:
            return self._get_json_respones({'result':'error'})

        uid=long(uid)
        author=source_author.objects.get(uid__exact=uid)
        form = AuthorForm(instance=author)
        c = RequestContext(request, {'form':form})
        tt = loader.get_template('sync_author_edit.html')
        return HttpResponse(tt.render(c))

    def post(self,request,uid,*args,**kwargs):
        user=request.user
        if not user.is_staff:
            return self._get_json_respones({'result':'error'})
        
        uid=long(uid)
        author=source_author.objects.get(uid__exact=uid)
        form = AuthorForm(instance=author,data=request.POST)
        if form.is_valid():
            form.save()
            return self._get_json_respones({'result':'success'})
        else:
            return self._get_json_respones({'result':'failed',
                                        'errors':form.errors})