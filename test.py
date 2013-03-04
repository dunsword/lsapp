# -*- coding: utf-8 -*-
'''
Created on 2012-7-3

@author: lihao
'''
import top.api 

'''
这边可以设置一个默认的appkey和secret，当然也可以不设置
注意：默认的只需要设置一次就可以了

'''
top.setDefaultAppInfo("21285955", "06b43aad22d457c583339f577904ec8a")

'''
使用自定义的域名和端口（测试沙箱环境使用）
a = top.api.UserGetRequest("gw.api.tbsandbox.com",80)

使用自定义的域名（测试沙箱环境使用）
a = top.api.UserGetRequest("gw.api.tbsandbox.com")

使用默认的配置（调用线上环境）
a = top.api.UserGetRequest()

'''
req = top.api.ItemGetRequest()
req.fields=('num_iid,title,price,has_discount,item_img,desc')
req.num_iid=16073374040
'''
可以在运行期替换掉默认的appkey和secret的设置
a.set_app_info(top.appinfo("appkey","*******"))
'''



try:
    f= req.getResponse()
    desc=f[u'item_get_response'][u'item'][u'desc']
    print len(desc)
    print(desc)
except Exception,e:
    print(e)
    
