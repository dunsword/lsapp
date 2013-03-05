# coding=utf-8
'''
Created on 2012-11-29

@author: DELL
'''
import sbs.api


file=open('d:/image.jpg','rb')
fd=file.read()
file.close()

publishReq = sbs.api.ThreadRequest(tokenId='100', tokenSecret='accessTest7118jqq54113accessTest', accessToken='100|30709440|c72c0814e20b46a25189443bc02b9729')
resp=publishReq.fileUpload(fd)


print resp
