# coding=utf-8
import urllib
import json

SBS_API_URL='http://www.19lou-inc.com/api/'
SBS_API_ENCODE='gbk'

def dataToReqeustStr(reqData):
    data=''
    for key in reqData.keys():
        value=reqData[key]
        if isinstance(value,unicode):
            value=urllib.quote(value.encode(SBS_API_ENCODE))
        else:
            value=unicode(value)
        data+=key+'='+value+'&'
    return data;

def postReqData(url,reqData):
    reqStr=dataToReqeustStr(reqData)
    print reqStr
    f=urllib.urlopen(url, reqStr)
    result=f.read()
    u_result = result.decode(SBS_API_ENCODE)
    jsonResult=json.loads(result,SBS_API_ENCODE)
    return jsonResult


#d={'key1':'value1','key2':'中文'}

#print dictToReqeustData(d)