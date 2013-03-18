# coding=utf-8

    
from django import forms
from ls.models import Feed

class DocumentForm(forms.Form):
    docid=forms.IntegerField(lable='docid',widget=forms.Field.hidden_widget)
    author_name=forms.CharField(
                               label='作者',
                               min_length=3,
                               max_length=100,
                               error_messages={
                                               'required': '昵称不能为空！',
                                               'min_length':'不能少于3个字！',
                                               'max_length': '不能超过100个字！'
                                               })
    title=forms.CharField(
                               label='标题',
                               min_length=1,
                               max_length=256,
                               error_messages={
                                               'required': '昵称不能为空！',
                                               'min_length':'标题不能为空！',
                                               'max_length': '不能超过256个字！'
                                               })
    content=forms.CharField(
                               label='内容摘要',
                               min_length=10,
                               max_length=1024,
                               error_messages={
                                               'required': '昵称不能为空！',
                                               'min_length':'不能少于10个字！',
                                               'max_length': '不能超过1024个字！'
                                               })
    created_at=forms.DateTimeField(label="创建时间",input_formats='%Y-%m-%d %H:%M:%S')
    update_status=forms.IntegerField(label="更新状态",input_formats='%Y-%m-%d %H:%M:%S')
    read_count=forms.IntegerField(label="阅读数")
    like_count=forms.IntegerField(label="喜欢数")
    reply_count=forms.IntegerField(label="回复数")
    
    categoryid=forms.IntegerField(label="类别")
    
class RecommendFeedForm(DocumentForm):
    feed_type=1
    feedid=forms.IntegerField(lable='feedid',widget=forms.Field.hidden_widget)
    username = forms.CharField(max_length=100,
                               label='用户名',
                               min_length=3,
                               max_length=100,
                               error_messages={
                                               'required': '昵称不能为空！',
                                               'min_length':'不能少于3个字！',
                                               'max_length': '不能超过100个字！'
                                               })
    userid = forms.IntegerField(label='uid')
    feed_created_at=forms.DateTimeField(label="创建时间",input_formats='%Y-%m-%d %H:%M:%S')
    
    def __init__(self):
        self.data
    
    
    
   
    
