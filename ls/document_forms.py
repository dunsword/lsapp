# coding=utf8
'''
Created on 2013-3-22

@author: paul
'''
from django import forms
from ls.models import Document,Topic,Category



class DocumentForm(forms.ModelForm):
    class Meta:
        model=Document
            
class DocumentService():
    def getHotDocuments(self,categoryid=None,size=20):
        '''
        TODO需要重构
        '''
        if categoryid:
            cat = Category.objects.get(pk=categoryid)
            if cat.level==1:
                q=Document.objects.select_related().filter(topic__catid_parent__exact=categoryid)[:size]
            else:
                q=Document.objects.select_related().filter(topic__categoryid__exact=categoryid)[:size]
            #q=Topic.objects.filter(categoryid__exact=categoryid)
            #q=q.filter(topic_type__exact=2)[:size]
            return q
        else:
            docs=Topic.objects.filter()[:size]