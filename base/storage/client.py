# coding=utf-8
#import sae.storage

class StorageClient(object):
    '''
       图片存储处理包，封装新浪SAE客户端或者本地文件存储 
    '''
    def __init__(self):
        #self.client=sae.storage.Client()
        pass
    
    def store(self, fileData):
        #obj = sae.storage.Object(fileData)
        #self.client.put('avatar', '001.jpg', obj)
        return ""#self.client.url('avatar','001.jpg')
        