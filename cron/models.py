from django.db import models

# Create your models here.

class  PageInfo(models.Model):
    #name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    content = models.TextField()
    word_count = models.BigIntegerField
    update_date = models.DateField()

