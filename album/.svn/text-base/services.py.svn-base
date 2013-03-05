'''
Created on 2012-11-29

@author: DELL
'''
import top.api
import re
import HTMLParser
'''
http://gw.api.tbsandbox.com/router/rest?
sign=57C25FF3FA926F392FDC494BD7AF2BDD&timestamp=2012-11-29+15%3A20%3A40&v=2.0&
app_key=1012129701&method=taobao.item.get&
partner_id=top-apitools&format=xml&num_iid=16073374040&
fields=detail_url,num_iid,title,nick,type,cid,seller_cids,
props,input_pids,input_str,desc,pic_url,num,valid_thru,
list_time,delist_time,stuff_status,location,price,post_fee,
express_fee,ems_fee,has_discount,freight_payer,has_invoice,
has_warranty,has_showcase,modified,increment,approve_status,
postage_id,product_id,auction_point,
property_alias,item_img,prop_img,sku,video,outer_id,is_virtual
'''
top.setDefaultAppInfo("21285955", "06b43aad22d457c583339f577904ec8a")
TAOBAO_URL_PATTERN=re.compile('id=\d{1,30}')

def getTaobaoItemId(taobaoItemUrl):
     m=re.search(TAOBAO_URL_PATTERN, taobaoItemUrl)
     if m is not None:
           id=m.group()[3:]
           return id
     else:
        return None 
    
def taobaoResult2Doc(result,doc):
    doc.title=result[u'item_get_response'][u'item'][u'title']
    doc.price=result[u'item_get_response'][u'item'][u'price']
    
    desc=result[u'item_get_response'][u'item'][u'desc']
    htmlParser=TaobaoDescParser()
    htmlParser.feed(desc)
    doc.content=htmlParser.pureText
    return doc
    
class DocumentService:
    def syncDocument(self,doc):
        taobaoId=getTaobaoItemId(doc.source)
        
        if taobaoId is None:
            return None#update failed
        
        req = top.api.ItemGetRequest()
        req.fields=('num_iid,title,price,has_discount,item_img,desc')
        req.num_iid=taobaoId
        try:
            f= req.getResponse()
            taobaoResult2Doc(f, doc)
            doc.save()
            return doc
        except Exception,e:
            print(e)
            return None
   
        
class TaobaoDescParser(HTMLParser.HTMLParser):
    pureText=''
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        
    #def handle_starttag(self, tag, attrs):
            
    def handle_data(self, data):
        self.pureText+=data
    
        