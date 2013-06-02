'''
Created by auto_sdk on 2012-11-22 16:33:41
'''
from api.top.api.base import RestApi
class WidgetAppapiruleCheckRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.api_name = None

	def getapiname(self):
		return 'taobao.widget.appapirule.check'
