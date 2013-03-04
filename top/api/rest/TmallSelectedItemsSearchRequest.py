'''
Created by auto_sdk on 2012-11-22 16:33:41
'''
from top.api.base import RestApi
class TmallSelectedItemsSearchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cid = None

	def getapiname(self):
		return 'tmall.selected.items.search'
