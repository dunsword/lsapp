# coding=utf-8
'''
Created on 2012-11-29

@author: Paul Wang <wagzhi@gmail.com>
'''
class appinfo(object):
    def __init__(self,appId,appSecret,upChennel,upAppName,upToken,encode='gbk'):
        self.appId = appId
        self.appSecret = appSecret
        self.encode = encode
        #附件上传接口参数
        self.upChennel=upChennel
        self.upAppName=upAppName
        self.upToken=upToken
        
def getDefaultAppInfo():
    pass

     
def setDefaultAppInfo(appId,appSecret,upChennel,upAppName,upToken,encode='gbk'):
    default = appinfo(appId,appSecret,upChennel,upAppName,upToken,encode='gbk')
    global getDefaultAppInfo 
    getDefaultAppInfo = lambda: default
    