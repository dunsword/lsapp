# coding=utf-8
from django.views.generic.base import View
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
import os
from django.template import RequestContext
from base.models import User,UserFollow
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from ls.models import Feed,Document,Category
from ls.feed_forms import RecommendFeedForm
from django.utils.decorators import method_decorator

class FeedShareView(View):
    
    @method_decorator(login_required)
    def post(self,request, *args, **kwargs):
        user=request.user
        feeds=self._get_feed_items(user.id,self.page_size)
        follows=self._get_follows(user.id, 20)
        c = RequestContext(request, {'feeds':feeds,'follows':follows})
        tt = loader.get_template('ls_index.html')
        return HttpResponse(tt.render(c))
    
    def get(self,request, *args, **kwargs):
        feedForm=RecommendFeedForm()
        c = RequestContext(request, {'feedForm':feedForm})
        tt = loader.get_template('ls_add_feed.html')
        return HttpResponse(tt.render(c))

class FeedShareService():
    def addRecommedFeed(self,user,recommendFeedForm):
        form = RecommendFeedForm()
        doc=Document();
        doc.categoryid=form.cleaned_data['categoryid']
        doc.title=form.cleaned_data['title']
        doc.author_name=form.cleaned_data['author_name']
        doc.content=form.cleaned_data['content']
        doc.created_at=form.cleaned_data['created_at']
        doc.updated_at=form.cleaned_data['updated_at']
        doc.read_count=form.cleaned_data['read_count']
        doc.reply_count=form.cleaned_data['reply_count']
        doc.like_count=form.cleaned_data['like_count']
        
        doc.save()
        
        feed=Feed()
        feed.userid=user.id
        feed.username=user.username
        feed.created_at=datetime.now()
        feed.feed_type=RecommendFeedForm.feed_type
        feed.save()
