from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Album(models.Model):
    name=models.CharField(max_length=200)
    desc=models.CharField(max_length=500)
    user=models.ForeignKey(User)
    pub_date=models.DateTimeField(auto_now=True,auto_now_add=True)
    last_new=models.DateTimeField(auto_now=True,auto_now_add=True)
    
class Document(models.Model):
    title=models.CharField(max_length=200)
    content=models.CharField(max_length=10000)
    source=models.CharField(max_length=500)
    price=models.FloatField()
    author=models.ForeignKey(User)
    album=models.ForeignKey(Album)
    pub_date=models.DateTimeField(auto_now=True,auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True,auto_now_add=True)
    class Meta:
        #abstract = True
        pass


    
