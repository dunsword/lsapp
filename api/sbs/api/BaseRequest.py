# coding=utf-8
import urllib
import json
from api import sbs


class BaseRequest:
    SBS_API_URL='http://www.19lou.com/api/'
    
    def __init__(self):
        self.clientId= sbs.getDefaultAppInfo().appId
        self.clientSecret= sbs.getDefaultAppInfo().appSecret
        self.upChennel= sbs.getDefaultAppInfo().upChennel
        self.upAppName= sbs.getDefaultAppInfo().upAppName
        self.upToken= sbs.getDefaultAppInfo().upToken
        self.encode= sbs.getDefaultAppInfo().encode
    
    def postReqData(self,url,reqData):
        '''
        url是请求参数
        reqData是请求参数的dict实例
        
                     返回转换为dict的json对象
        '''
        reqStr=self.dataToReqeustStr(reqData)
        print reqStr
        f=urllib.urlopen(url, reqStr)
        result=f.read()
        jsonResult=json.loads(result,self.encode)
        return jsonResult
    
    def dataToReqeustStr(self,reqData):
        data=''
        for key in reqData.keys():
            value=reqData[key]
            if isinstance(value,unicode):
                value=urllib.quote(value.encode(self.encode))
            else:
                value=unicode(value)
            data+=key+'='+value+'&'
        return data;