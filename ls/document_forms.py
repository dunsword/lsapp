# coding=utf8
'''
Created on 2013-3-22

@author: paul
'''
from django import forms
from ls.models import Document



class DocumentForm(forms.ModelForm):
    class Meta:
        model=Document
            
class DocumentService():
    def getHotDocuments(self,categoryid=None,size=20):
        '''
        TODO需要重构
        '''
        if categoryid:
            docs=Document.objects.filter(categoryid__exact=categoryid)[:size]
            return docs
        else:
            docs=Document.objects.filter()[:size]