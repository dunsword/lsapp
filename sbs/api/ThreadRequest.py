'''
Created on 2012-12-10

@author: DELL
'''
import config
import utils
import urllib
import json
from sbs.api.BaseRequest import BaseRequest
import httplib

PUBLISH_REQUEST_URL=BaseRequest.SBS_API_URL+'thread/publishThread'
GET_THREAD_VIEW_REQUEST_URL=BaseRequest.SBS_API_URL+'thread/getThreadView'
FILE_UPLOAD_REQUEST_URL=BaseRequest.SBS_API_URL+'user/fileUpload'

class ThreadRequest(BaseRequest):    
    def __init__(self,accessToken):
        BaseRequest.__init__(self)
        self.accessToken=accessToken
        
    def getThreadView(self,fid,tid,page=1,perPage=30):
        reqData={
                 'fid':fid,
                 'tid':tid,
                 'page':page,
                 'perPage':perPage,
                 'client_id':self.clientId,
                 'client_secret':self.clientSecret,
                 }
        return config.postReqData(GET_THREAD_VIEW_REQUEST_URL, reqData)
    
    def fileUpload(self,fd):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
#        fields={'access_token':self.accessToken,}  
#        ffs={'file':file}
#        content_type, body = utils.getMutiFormBodyData(fields,ffs)
#        h = httplib.HTTPConnection('www.19lou.com',80)
#        #h.p
#        #h.request('POST', '/api/user/fileUpload', body, {'content-type':content_type,'content-length': str(len(body))})
#        h.putrequest('POST', '/api/user/fileUpload')
#        h.putheader('content-type', content_type)
#        h.putheader('content-length', str(len(body)))
#        h.endheaders()
#        h.send(body)
        #errcode, errmsg, headers = h.getreply()
        reqStr='access_token='+self.accessToken+'&file=aa'
        print reqStr
        f=urllib.urlopen('http://www.19lou.com/api/user/fileUpload', reqStr)
        result=f.read()
        u_result = result.decode(config.SBS_API_ENCODE)
        jsonResult=json.loads(result,config.SBS_API_ENCODE)
        return jsonResult


    
    
    def publishThread(self,fid,subject,content,threadcategory=0):
        reqData={
                 'fid':fid,
                 'subject':subject,
                 'content':content,
                 'threadcategory':threadcategory,
                 'access_token':self.accessToken,
                 }
        return config.postReqData(PUBLISH_REQUEST_URL, reqData)
        