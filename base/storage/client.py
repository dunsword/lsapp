# coding=utf-8
from django.conf import settings
from datetime import datetime
from PIL import Image
from StringIO import StringIO


class StorageClient():
    DOMAIN_AVATOR="avatar"
    DOMAIN_ATTACH="attach"

    SIZE_MIDDLE='middle'
    SIZE_60='60X60'
    SIZE_250='250X250'
    
    #所有定义的尺寸列表
    SIZE_DICT = {
                 SIZE_60:{60,60},
                 SIZE_250:{250,250},
                 SIZE_MIDDLE:{600,1080}
                }
    

    def __init__(self,domain,supportedSizes=None):
        try:
            import sae.storage
            self.storage=sae.storage
            self.client=sae.storage.Client()
        except RuntimeError, e:
            self.client=None
            self.storage=None
        
        self.domain = domain
        self.supportedSizes=supportedSizes
    
    def store(self, uid,file):
        #obj = sae.storage.Object(fileData)
        #self.client.put('avatar', '001.jpg', obj)
        
        fileName=self.getSaveFileName(uid,file.name)
        fullPathName=self.getStoreFileName(fileName)
       
        if self.client==None:
            im=Image.open(file)
            im.save(fullPathName,"JPEG",quality=100)
           
        else:
            
            data=file.read();
            
            ob = self.storage.Object(data)
            try:
                self.client.delete(self.domain, fileName)
            except self.storage.ObjectNotExistsError,e:
                pass
            self.client.put(self.domain, fileName, ob)
        return fileName
        #self.client.url('avatar','001.jpg')
    
    def getStoreFileName(self,fileName):        
        return settings.STATIC_ROOT+self.domain+"/"+fileName
        
    def url(self,fileName,size=None):
        sFileName=None;
        if size:
            sFileName=size+"_"+fileName
        else:
            sFileName=fileName
    
        if self.client==None:
            return settings.STATIC_URL+self.domain+"/"+sFileName
        else:
            return self.client.url(self.domain, sFileName)
    
    def getSaveFileName(self,uid,originName=None):
        '''
                        根据yy_mm_dd_hh_mm_ss_uid_originName生成文件名，
                        如果用户同时提交两个相同文件名，会覆盖.
                        由于包含UID，不支持未登录用户上传
         TODO：暴露UID不好
        '''
        now=datetime.now()
        if originName == None:
            originName = 'none.jpg'
        elif len(originName) > 10: #避免文件名过长，截取后面10个字符
            originName = originName[len(originName)-10:]
        return now.strftime('%y_%m_%d_%H_%M_%S_')+str(uid)+'_'+str(originName)    

class CAvatarStorageClient(StorageClient):
    PREFIX="a_o_"
    def getSaveFileName(self,uid,originName=None):
        return CAvatarStorageClient.PREFIX+str(uid)+".jpg"
        
class CAvatarCropClient(StorageClient):
    PREFIX="a_250X250_"
    def getDefaultAvatarUrl(self,size=StorageClient.SIZE_250):
        return settings.STATIC_URL+self.domain+"img/avatar_default.jpg"
        
    def getSaveFileName(self,uid,originName=None):
#        now=datetime.now()
#        prefix="a_"+now.strftime('%y_%m_%d_%H_%M_%S_')
        return CAvatarCropClient.PREFIX+str(uid)+".jpg"
    
    def store(self, uid,fileName,displayW,displayH,left,top,cropW,cropH):
        #obj = sae.storage.Object(fileData)
        #self.client.put('avatar', '001.jpg', obj)
        if self.client==None:
            fullName = self.getStoreFileName(fileName)
            im=Image.open(fullName)
        else:
            ob = self.client.get(self.domain, fileName)
            
            datain=StringIO()
            datain.write(ob.data)
            datain.seek(0)
            im=Image.open(datain)
            
        im.thumbnail((displayW,displayH), Image.ANTIALIAS)
        area=im.crop((left,top,left+cropW,top+cropH))
        
        fileName=self.getSaveFileName(uid)

       
        area.thumbnail((250,250),Image.ANTIALIAS)
        
        if self.client==None:
            fullPathName=settings.STATIC_ROOT+self.domain+"/"+fileName
            area.save(fullPathName,"JPEG",quality=100)
        else:
            out=StringIO()
            area.save(out,"JPEG",quality=100)
            ob = self.storage.Object(out.getvalue())
            
            try:
                self.client.delete(self.domain, fileName)
            except :
                pass
            
            self.client.put(self.domain, fileName, ob)
         
        return fileName#self.client.url('avatar','001.jpg')
        

   
     
AvatarClient=CAvatarStorageClient("avatar")
CropClient=CAvatarCropClient("avatar")
#
#class ImageClient(StorageClient):
#    URL_ROOT=settings.STATIC_URL
#    STORAGE_ROOT=settings.STATIC_ROOT
#    '''
#       图片存储处理包，封装新浪SAE客户端或者本地文件存储 
#    '''
#    def __init__(self,domain,supportedSize):
#        #self.client=sae.storage.Client()
#        self.domain=domain
#    
#    def store(self, uid,file,originName):
#        #obj = sae.storage.Object(fileData)
#        #self.client.put('avatar', '001.jpg', obj)
#        im=Image.open(file)
#        fileName=self.nameStratage(uid,originName)
#        im.save(fileName,"JPEG",quality=100)
#        for size in self.supportedSize:
#            sizeFileName=size+"_"+fileName
#            dm=StorageClient.SIZE_DICT[size]
#            sizeIm=im.resize(dm,Image.ANTIALIAS) #TODO需要优化，目前会变形，需要添加按比例截取的功能
#            sizeIm.save(sizeFileName,"JPEG",quality=100)
#            
#        return fileName#self.client.url('avatar','001.jpg')
#        
#    def url(self,fileName):
#        return ImageClient.URL_ROOT+self.domain+"/"+fileName
#    
#    def thrumbURL(selfs,fileName,size):
#        if size in self.supportedSzie:
#            return ImageClient.URL_ROOT+self.domain+"/"+size+'_'+fileName
#        else:
#            return None
#    
#
#        
#    

