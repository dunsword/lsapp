'''
Created by auto_sdk on 2012-11-22 16:33:41
'''
from api.top.api.base import RestApi
class TaobaokeWidgetItemsConvertRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.is_mobile = None
		self.num_iids = None
		self.outer_code = None
		self.track_iids = None

	def getapiname(self):
		return 'taobao.taobaoke.widget.items.convert'
