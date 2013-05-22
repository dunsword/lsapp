# coding=utf-8
__author__ = 'paul'

from django.views.generic.base import View
import hashlib, time, re
from xml.etree import ElementTree as ET
from django.http import HttpResponse

class WeixinTokenInvalidView(View):
     def get(self,request,*args, **kwargs):
            token = "dwmbnzjdqejltmndt"
            params = request.GET
            args = [token, params['timestamp'], params['nonce']]
            args.sort()
            if hashlib.sha1("".join(args)).hexdigest() == params['signature']:
                if params.has_key('echostr'):
                     return HttpResponse(params['echostr'])

            return HttpResponse('failed')


