# coding=utf-8
'''
Created on 2012-11-26

@author: DELL
'''
from django import forms
from django.contrib.auth.models import User

my_default_errors = {
    'required': '该项不能为空！',
    'invalid': '该项数据不合法！'
}

class RegisterUserForm(forms.Form):
    username=forms.CharField(max_length=100,label='用户名',error_messages=my_default_errors)
    email=forms.EmailField(label='电子邮箱',error_messages=my_default_errors)
    password=forms.CharField(widget=forms.PasswordInput,label='密 码',error_messages=my_default_errors)
    repassword=forms.CharField(widget=forms.PasswordInput,label='重新输入密码',error_messages=my_default_errors)
    
    
    def clean_username(self):
        username=self.cleaned_data['username']
        if len(username)<3:
            raise forms.ValidationError('用户名不能小于3个字符！')
        try:
            user=User.objects.get(username=username)
            raise forms.ValidationError('用户名已经存在！')
        except User.DoesNotExist:
            pass
        return username
    def clean_password(self):
        password=self.cleaned_data['password']
        if len(password)<4:
            raise forms.ValidationError('密码不能小于4个字符')
        return password
    def clean_repassword(self):
        password=None
        try:
            password=self.cleaned_data['password']
        except:
            pass
        repassword=self.cleaned_data['repassword']
            
        if password!=None and password!=repassword:
                raise forms.ValidationError('两次输入的密码不一致！')
        return password
        
        
    
    def clean_email(self):
        email=self.cleaned_data['email']
        try:
            user=User.objects.get(email=email)
            raise forms.ValidationError('该电子邮箱已经被使用！')
        except User.DoesNotExist:
            return email
class SetupForm(forms.Form):
    firstName=forms.CharField(max_length=20,label='姓')
    lastName=forms.CharField(max_length=20,label='名')
    avatar=forms.FileField()
    
class LoginForm(forms.Form):
    username=forms.CharField(max_length=100,label='用户名',error_messages={'required':'请输入用户名!'})
    password=forms.CharField(widget=forms.PasswordInput,label='密  码',error_messages={'required':'请输入密码！'})
    