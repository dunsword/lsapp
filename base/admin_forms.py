# coding=utf-8
'''
Created on 2013-2-4

@author: paul
'''
from django import forms
from django.contrib.auth.models import User

class UserEditForm(forms.Form):
    
    my_default_errors = {
                         'required': '该项不能为空！',
                         'invalid': '该项数据不合法！'
    }
    
    username = forms.CharField(max_length=100, label='用户名', error_messages=my_default_errors)
    email = forms.EmailField(label='电子邮箱', error_messages=my_default_errors)
    #password = forms.CharField(widget=forms.PasswordInput, label='密 码', error_messages=my_default_errors)
    last_name = forms.CharField(max_length=100, label='姓')
    first_name = forms.CharField(max_length=100, label='名')
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError('用户名不能小于3个字符！')
        
        return username
    
#    def clean_password(self):
#        password = self.cleaned_data['password']
#        if len(password) < 4:
#            raise forms.ValidationError('密码不能小于4个字符')
#        return password      
        
    
    def clean_email(self):
        email = self.cleaned_data['email']
        return email
