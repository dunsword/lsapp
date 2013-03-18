# coding=utf-8
from django.views.generic.base import View
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.template import RequestContext
from base.models import User
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ls.models import Feed,Document,Category
from django.utils.decorators import method_decorator

class FeedView(View):
    page_size=20
    
    @method_decorator(login_required)
    def get(self,request, *args, **kwargs):
        user=request.user
        feeds=self._get_feed_items(user.id,self.page_size)
        c = RequestContext(request, {'feeds':feeds})
        tt = loader.get_template('ls_index.html')
        return HttpResponse(tt.render(c))
    
    def _get_feed_items(self,uid,page_size):
        items=[]
        feeds=Feed.objects.all()[0:self.page_size]
        for feed in feeds:
            author=User.objects.get(pk=feed.userid)
            document=Document.objects.get(pk=feed.docid)
            category=Category.objects.get(pk=document.categoryid)
            item=FeedItem(author,feed,document,category)
            items.append(item)
        return items
    
class FeedItem():
    def __init__(self,author,feed,document,category):
        self.category=category
        self.document=document
        self.feed=feed
        self.author=author
