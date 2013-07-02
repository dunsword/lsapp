# coding=utf-8
'''
Created on 2013-2-22

@author: paul
'''
from base.models import User
from api.auth19 import Auth,AuthResult
from datetime import datetime


class BaseBackend(object):
    def __init__(self):
        self.auth19=Auth()

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            result=self.auth19.authenticate(username,password)

            if result!=None:
                userInfo=self.auth19.getUserInfo(result.access_token)
                gender=1
                if userInfo.gender==u'male':
                    gender=2
                user=User.objects.create_user(username=username,email=userInfo.email,password=password,nickname=username,gender=gender)
                return user
            return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
        