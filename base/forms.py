# coding=utf-8
'''
Created on 2012-11-26

@author: DELL
'''
from django import forms
from base.models import User

my_default_errors = {
    'required': '该项不能为空！',
    'invalid': '该项数据不合法！'
}

class RegisterUserForm(forms.Form):
    username = forms.CharField(max_length=100, 
                               label='用户名', 
                               error_messages=my_default_errors, 
                               widget=forms.TextInput(attrs={'placeholder': u'3-10个字母、数字或汉字'}))
    email = forms.EmailField(label='电子邮箱', error_messages=my_default_errors,widget=forms.TextInput(attrs={'placeholder': u'请输入正确的邮箱地址'}))
    password = forms.CharField(widget=forms.PasswordInput, label='密 码', error_messages=my_default_errors)
    repassword = forms.CharField(widget=forms.PasswordInput, label='确认密码', error_messages=my_default_errors)
    
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 3:
            raise forms.ValidationError('用户名不能小于3个字符！')
        try:
            user = User.objects.get(username__exact=username)
            raise forms.ValidationError('用户名已经存在！')
        except User.DoesNotExist:
            pass
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 4:
            raise forms.ValidationError('密码不能小于4个字符')
        return password
    def clean_repassword(self):
        password = None
        try:
            password = self.cleaned_data['password']
        except:
            pass
        repassword = self.cleaned_data['repassword']
            
        if password != None and password != repassword:
                raise forms.ValidationError('两次输入的密码不一致！')
        return password
        
        
    
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError('该电子邮箱已经被使用！')
        except User.DoesNotExist:
            return email
        
        
class UserForm(forms.ModelForm):
    #password=forms.CharField(label=u'密码',required=False,widget=forms.PasswordInput)
    class Meta:
            model=User
            exclude = ('avatar','password')
            widgets = {
              #'password':forms.PasswordInput
            }
            
class SetupForm(forms.Form):
#    firstName = forms.CharField(
#                              widget=forms.TextInput(attrs={'placeholder': u'请输入姓名'}),
#                              max_length=8,
#                              label=u'姓名',
#                              required=False,
#                              initial='姓名',
#                              error_messages={'max_length': '名字不能超过8个字！', })
    #lastName=forms.CharField(max_length=20,label='名')
    nickname = forms.CharField(
                               widget=forms.TextInput(attrs={'placeholder': u'请输入昵称'}),
                               min_length=3,
                               max_length=20,
                               label=u"昵称",
                               error_messages={
                                               'required': '昵称不能为空！',
                                               'min_length':'不能少于3个字！',
                                               'max_length': '不能超过20个字！'
                                               })
    gender = forms.IntegerField(widget=forms.RadioSelect(choices=[(1,u'女'),(2,u'男'),(3,u'保密')]))
    #email=forms.EmailField(label='电子邮箱')
    #avatar=forms.FileField()
    
class SetAvatarForm(forms.Form):
    avatar=forms.FileField()
    
class SetpassForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, label=u'原密码', error_messages={'required':'必须输入原密码！'})
    #lastName=forms.CharField(max_length=20,label='名')
    newPassword = forms.CharField(widget=forms.PasswordInput, min_length=4, max_length=20, label=u"新密码", error_messages={
    'required': '新密码不能为空！',
    'min_length':'不能少于4个字！',
    'max_length': '不能超过20个字！'})
    rePassword = forms.CharField(widget=forms.PasswordInput, min_length=4, max_length=20, label=u"确认新密码", error_messages={
    'required': '确认密码不能为空！',
    'min_length':'不能少于4个字！',
    'max_length': '不能超过20个字！'})
    def clean_rePassword(self):
        password = None
        try:
            password = self.cleaned_data['newPassword']
        except:
            pass
        repassword = self.cleaned_data['rePassword']
            
        if password != None and password != repassword:
                raise forms.ValidationError('密码不一致！')
        return password


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='用户名', error_messages={'required':'请输入用户名!'})
    password = forms.CharField(widget=forms.PasswordInput, label='密  码', error_messages={'required':'请输入密码！'})
    remember = forms.BooleanField(widget=forms.CheckboxInput ,label='记住密码')
    
