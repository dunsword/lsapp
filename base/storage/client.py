# coding=utf-8
from django.conf import settings
from datetime import datetime
from PIL import Image
#import sae.storage
class StorageClient():
    OMAIN_AVATOR="avatar"
    DOMAIN_ATTACH="attach"
    #下面两个实例可以根据需要切换
    #if defalut
    __avatarClient__=ImageClient(DOMAIN_AVATOR)
    __attachClient__=ImageClient(DOMAIN_ATTACH)
    
    SIZE_MIDDLE='middle'
    SIZE_60='60X60'
    
    SIZE_DICT = {SIZE_60:(60,60)}
    
    
    #else if sae
    #sae implements
    
    def getAvatarClient():
        return __avatarClient__
    
    def getAttachClient():
        return __attachClient__

class ImageClient(StorageClient):
    URL_ROOT=settings.STATIC_URL
    STORAGE_ROOT=settings.STATIC_ROOT
    '''
       图片存储处理包，封装新浪SAE客户端或者本地文件存储 
    '''
    def __init__(self,domain,supportedSize):
        #self.client=sae.storage.Client()
        self.domain=domain
    
    def store(self, uid,file,originName):
        #obj = sae.storage.Object(fileData)
        #self.client.put('avatar', '001.jpg', obj)
        im=Image.open(file)
        fileName=self.nameStratage(uid,originName)
        im.save(fileName,"JPEG",quality=100)
        for size in self.supportedSize:
            sizeFileName=size+"_"+fileName
            dm=StorageClient.SIZE_DICT[size]
            sizeIm=im.resize(dm,Image.ANTIALIAS) #TODO需要优化，目前会变形，需要添加按比例截取的功能
            sizeIm.save(sizeFileName,"JPEG",quality=100)
            
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
        
    