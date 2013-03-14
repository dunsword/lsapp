# coding=utf-8
from django.conf import settings
from datetime import datetime
from PIL import Image
#import sae.storage
class StorageClient():
    DOMAIN_AVATOR="avatar"
    DOMAIN_ATTACH="attach"
    #下面两个实例可以根据需要切换
    #if defalut
    __avatarClient__=None
    __attachClient__=None
    
    SIZE_MIDDLE='middle'
    SIZE_60='60X60'
    
    SIZE_DICT = {SIZE_60:(60,60)}
    
    __inited__=False
    count=0
    @staticmethod
    def init():
        if not StorageClient.__inited__:
            StorageClient.__avatarClient__=ImageClient(StorageClient.DOMAIN_AVATOR,{StorageClient.SIZE_60})
            StorageClient.__attachClient__=ImageClient(StorageClient.DOMAIN_ATTACH,{})
            StorageClient.__inited__=True
        StorageClient.count=StorageClient.count+1
    
    @staticmethod   
    def isInited():
        inited=StorageClient.__inited__
        return inited    
    #else if sae
    #sae implements
    @staticmethod
    def getAvatarClient():
        return StorageClient.__avatarClient__
    
    @staticmethod
    def getAttachClient():
        return StorageClient.__attachClient__
    
    
    def store(self, uid,file,originName):
        '''
        store image file and thrumb files
        '''
        pass
    
   
    def url(self,fileName):
        '''
        return the url of the image file
        '''
        pass
    
   
    def thrumbURL(self,fileName,size):
        pass
    
class ImageClient(StorageClient):
    URL_ROOT=settings.STATIC_URL
    STORAGE_ROOT=settings.STATIC_ROOT
    '''
       图片存储处理包，封装新浪SAE客户端或者本地文件存储 
    '''
    def __init__(self,domain,supportedSize):
        #self.client=sae.storage.Client()
        self.supportedSize=supportedSize
        self.domain=domain
    
    def store(self, uid,file,originName):
        #obj = sae.storage.Object(fileData)
        #self.client.put('avatar', '001.jpg', obj)
        im=Image.open(file)
        fileName=self.nameStratage(uid,originName)
        fullName=ImageClient.STORAGE_ROOT+self.domain+"/"+fileName
        im.save(fullName,"JPEG",quality=100)
        for size in self.supportedSize:
            sizeFileName=size+"_"+fileName
            dm=StorageClient.SIZE_DICT[size]
            sizeIm=im.resize(dm,Image.ANTIALIAS) #TODO需要优化，目前会变形，需要添加按比例截取的功能
            sizeIm.save(ImageClient.STORAGE_ROOT+self.domain+"/"+sizeFileName,"JPEG",quality=100)
            
        return fileName#self.client.url('avatar','001.jpg')
        
    def url(self,fileName):
        return ImageClient.URL_ROOT+self.domain+"/"+fileName
    
    def thrumbURL(selfs,fileName,size):
        if size in self.supportedSzie:
            return ImageClient.URL_ROOT+self.domain+"/"+size+'_'+fileName
        else:
            return None
    
    def nameStratage(self,uid,orginName):
        '''
        根据yy_mm_dd_hh_mm_ss_uid_originName生成文件名，
        如果用户同时提交两个相同文件名，会覆盖.
        由于包含UID，不支持匿名
        '''
        now=datetime.now()
        return now.strftime('%y_%m_%d_%H_%M_%S_')+str(uid)+'_'+str(orginName)
        
StorageClient.init()
