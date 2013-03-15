from django.db import models
from django.utils import timezone

# Create your models here.
class Feed(models.Model):
    userid=models.IntegerField('user id')
    username=models.CharField('user name',max_length=30)
    title=models.CharField('title',max_length=256)
    content=models.CharField('content',max_length=1024)
    created_at=models.DateTimeField('created time', default=timezone.now)
    read_count=models.IntegerField('read count',default=0)
    like_count=models.IntegerField('like count',default=0)
    reply_count=models.IntegerField('reply count',default=0)
    update_status=models.SmallIntegerField('status',default=0)