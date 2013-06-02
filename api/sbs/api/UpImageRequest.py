import time
import httplib
import hashlib
import json

from api import sbs
import utils

UP_URL='up.citysbs.com'

class UpImageRequest:
    def __init__(self):
        self.upChennel= sbs.getDefaultAppInfo().upChennel
        self.upAppName= sbs.getDefaultAppInfo().upAppName
        self.upToken= sbs.getDefaultAppInfo().upToken
        
    def upload(self,uid,file):
        now=str(int(time.time()))  
        suid=str(uid)
        '''
        t=md5(channel+appname+appkey+uid+time+wmurl+wmpos);
        '''
        rawtoken=self.upChennel+self.upAppName+self.upToken+suid+now
        m=hashlib.md5()
        m.update(rawtoken)
        md5token=m.hexdigest()
              
        fields={
                'channel':self.upChennel,
                'appname':self.upAppName,
                'uid':suid,
                'time':now,
                'info':'fid-1|albumid-1',
                'wmurl':'',
                'wmpos':'',
                't':md5token                
            }
        fileFields={'file':file}
        contentType,body= utils.getMutiFormBodyData(fields, fileFields)
      
        h = httplib.HTTPConnection(UP_URL,80)
        #h.p
        #h.request('POST', '/api/user/fileUpload', body, {'content-type':content_type,'content-length': str(len(body))})
        h.putrequest('POST', '/?DEBUG=1')
        h.putheader('content-type', contentType)
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        resp=h.getresponse()
        jsonstr=resp2json(resp.read())
        jsonObj=json.loads(jsonstr,'gbk')
        return jsonObj

import re
def resp2json(resp):
    p=re.compile("^<img src='[\w/\.:]*'/>")
    m=re.search(p, resp)
    if m is not None:
        imgTag=m.group()
        jsonResp=resp[len(imgTag):]
        jr2=jsonResp.replace('\/','/')
        return jr2
    return resp.replace('\/','/')#if regex search failed
'''
{
    "success":true,
    "code":0,
    "errcode":"10",
    "data":
        {
            "fileType":"jpg",
            "isImage":true,
            "aid":"14301355306829268",
            "fileSize":111505,
            "source":0,
            "name":"180709_14301355306829268_2caf95c7fe71e861cafcc4827380032e.jpg",
            "domain":"http:\/\/att2.citysbs.com\/qptest",
            "path":"\/2012\/12\/12\/18\/",
            "origName":"123.jpg",
            "thumb":"http:\/\/att3.citysbs.com\/120x120\/qptest\/2012\/12\/12\/18\/180709_14301355306829268_2caf95c7fe71e861cafcc4827380032e.jpg",
            "cost":0.063854932785,
            "width":448,
            "height":670
         }
}
    
'''


s='''<img src='http://att3.citysbs.com/120x120/qptest/2012/12/12/18/180709_14301355306829268_2caf95c7fe71e861cafcc4827380032e.jpg'/>{"success":true,"code":0,"errcode":"10","data":{"fileType":"jpg","isImage":true,"aid":"14301355306829268","fileSize":111505,"source":0,"name":"180709_14301355306829268_2caf95c7fe71e861cafcc4827380032e.jpg","domain":"http:\/\/att2.citysbs.com\/qptest","path":"\/2012\/12\/12\/18\/","origName":"123.jpg","thumb":"http:\/\/att3.citysbs.com\/120x120\/qptest\/2012\/12\/12\/18\/180709_14301355306829268_2caf95c7fe71e861cafcc4827380032e.jpg","cost":0.063854932785,"width":448,"height":670}}'''
print resp2json(s)
