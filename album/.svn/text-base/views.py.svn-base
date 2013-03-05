# coding=utf-8
from django.template import Context, loader
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.template import RequestContext
from album.models import Album,Document
from httplib import HTTPResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from album.services import DocumentService
from django.conf import settings


@login_required
def index(request):
    user=request.user
    q=Album.objects.filter(user__exact=user)
    album=None
    if q:
        album=q[0]
    else: #create a album
        album=Album()
        album.name=u'$'+user.username
        album.user=user
        album.save()
    
    items=Document.objects.filter(album__exact=album)

    c=RequestContext(request,{'user':user,'items':items,'album':album,'static':settings.STATIC_ROOT})
    c.update(csrf(request))
    tt = loader.get_template('index.html')
    return HttpResponse(tt.render(c))

@login_required
def add(request):
    theurl=request.POST['theurl']
    if theurl is not None:
        user=request.user
        album=Album.objects.get(name=u'$'+user.username)
        doc=Document()
        doc.author=user
        doc.album=album
        doc.price=0
        doc.title="淘宝商品"        
        doc.source=theurl
        ds=DocumentService()
        ds.syncDocument(doc)
        c=RequestContext(request,{'doc':doc})
        tt = loader.get_template('add.html')
        return HttpResponse(tt.render(c))



@login_required
def detail(request,doc_id):
    #TODO 检查是否当前用户
    doc=Document.objects.get(pk=doc_id)
    docSrv=DocumentService()
    doc=docSrv.syncDocument(doc)
    c=RequestContext(request,{'doc':doc})
    tt = loader.get_template('detail.html')
    return HttpResponse(tt.render(c))

@login_required
def detail_update(request,doc_id):
    #TODO 检查是否当前用户
    doc=Document.objects.get(pk=doc_id)
    c=RequestContext(request,{'doc':doc})
    tt = loader.get_template('detail.html')
    return HttpResponse(tt.render(c))