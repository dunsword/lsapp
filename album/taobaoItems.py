'''
Created on 2012-12-7

@author: DELL
'''
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class TaobaoItem(models.Model):
    name=models.CharField(max_length=200)
    desc=models.CharField(max_length=500)
    user=models.ForeignKey(User)
    pub_date=models.DateTimeField(auto_now=True,auto_now_add=True)
    last_new=models.DateTimeField(auto_now=True,auto_now_add=True)
    class Meta:
        app_label='album'
        managed=True
        