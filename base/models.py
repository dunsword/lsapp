# coding=utf-8

from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable, UNUSABLE_PASSWORD)
from django.conf import settings
from twisted.conch.test.test_insults import default
# from django.contrib.auth.models import User
# Create your models here.
# class UserProfileManager(models.Model):
#    def create_user(self,username,email,password):
#        User.objects.create(username,email,password)
#
#
# class UserProfile(models.Model):
#    objects=UserProfileManager()
#    class Meta:
#        permissions = (
#            ("admin_task", "Can manage users."),
#        )
#        
#    user=models.OneToOneField(User)

class UserManager(models.Manager):
    def create_user(self, username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user
    
    def getByEmail(self, email):
        return self.get(email=email)
        
class User(models.Model):
    objects = UserManager()
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('必须包含3-30个数字、英文字母或者下划线！'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    nickname = models.CharField(_('nick name'), max_length=30, unique=True)
    email = models.EmailField(_('e-mail address'), unique=True)
    avatar = models.URLField(_('avatar'), null=True)
    password = models.CharField(_('password'), max_length=128)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('确定是否管理员.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    is_superuser = models.BooleanField(_('superuser status'), default=False,
        help_text=_('超级用户，拥有所有权限'))
    last_login = models.DateTimeField(_('last login'), default=timezone.now)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    
    class Meta:
        # abstract = True
        pass
    def get_avatar_url(self):
        if self.avatar:
            return settings.STATIC_URL + "avatar/" + self.avatar
        else:
            return settings.STATIC_URL + "img/avatar_default.jpg"
            
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Returns a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            self.save()
        return check_password(raw_password, self.password, setter)
    
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

class UserFollow(models.Model):
    userid = models.IntegerField('user id')
    username = models.CharField('user Name', max_length=30,)
    followed_userid = models.IntegerField('followed user id')
    followed_username = models.CharField('followed user name', max_length=30,)
    class Meta:
        unique_together = (("userid", "followed_userid"),)

class User3rdInfo(models.Model):
    userid = models.IntegerField('user id')
    sid = models.CharField('user sid', max_length=50,)
    type = models.IntegerField('type')
    nick_name = models.CharField('nick name', max_length=50, blank=True)
    access_token = models.CharField('access token', max_length=50,)
    access_token_secret = models.CharField('access token secret', max_length=50,)
    access_updated_at = models.DateField('access_updated_at')
    feeds_type = models.CharField('feeds type', max_length=10, blank=True)
    reg_ip = models.IntegerField('reg ip', blank=True)
    status = models.IntegerField('status')
    expires_in = models.DateField('expires in')
    re_expires_in = models.DateField('expires in')
    refresh_token = models.CharField('refresh token', max_length=100, blank=True)
    verified = models.IntegerField('verified', blank=True)
    created_at = models.DateField('created at')
    updated_at = models.DateField('updated at')
    class Meta:
        unique_together = (("userid", "type"),)
    
