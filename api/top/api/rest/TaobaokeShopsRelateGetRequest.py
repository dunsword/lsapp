'''
Created by auto_sdk on 2012-11-22 16:33:41
'''
from api.top.api.base import RestApi
class TaobaokeShopsRelateGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.is_mobile = None
		self.max_count = None
		self.nick = None
		self.outer_code = None
		self.pid = None
		self.seller_id = None
		self.seller_nick = None
		self.shop_type = None
		self.sort = None

	def getapiname(self):
		return 'taobao.taobaoke.shops.relate.get'