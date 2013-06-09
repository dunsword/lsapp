# coding=utf-8
import logging
import sys,os
from httplib2 import Http
import json
from docfetcher import DocItem,DocumentList,SourceInfo

reload(sys)
sys.setdefaultencoding('utf-8')

class Huatan():
    client_id = 100
    client_secret = u"accessTest7118jqq54113accessTest"
    lou19Url = "https://www.19lou.com/api/board/getBoardThreadList?client_id=%d&client_secret=%s&filterWater=true"%(client_id,client_secret)
    httpHeaders = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
    imageBaseUrl = u"http://att3.citysbs.com/"
    imageSize = u"200x240"

    def getThreadList(self,bid,page=1,perPage=50):
        """
        花坛获得列表页接口
        :param bid:       花坛id
        :param page:      获得列表第几页
        :param perPage:   每页显示的条数
        :return:          字典
        """

        huatanUrl = self.lou19Url + "&bid=%s"%(str(bid))+"&page="+str(page)+"&perPage="+str(perPage)
        hClient = Http()
        headers = {"Content-type": "application/json", "Accept": "txt/plain","User-Agent": "Magic Browser"}
        resp, content = hClient.request(huatanUrl,"GET",headers=headers)
        content = content.decode('gb18030').encode('utf8')
        jsonContent = json.loads(content)
        #获得花坛的相关数据
        boardinfo = jsonContent["board"]
        boardName = boardinfo["name"]
        boardDesc = boardinfo["description"]
        categoryName = boardinfo["category"]["name"]
        cover = boardinfo["cover"]
        #获得帖子列表的相关数据
        htThreadlist = jsonContent["board_thread_list"]
        threadList = []
        for item in htThreadlist:
            tid=item['thread']['tid']
            reply_count=int(item['thread']['replies'])
            subject = item["subject"]
            content = item["content"]
            cityName = item["city_name"]
            images = []
            tmp  = item["images"]
            imgs = tmp[1:len(tmp)-1].split(",")
            for img in imgs:
                images.append(self.imageBaseUrl + self.imageSize + "/" +cityName + img[1:len(img)-1])

            created_at = item["created_at"]
            url = item["outsite_url"]

            docItem=DocItem(tid=tid,uid=0,
                            content=content,
                            subject=subject,
                            url=url,
                            tags='',
                            reply_count=reply_count,
                            view_count=0,created_at=created_at)
            threadList.append(docItem)

        si=SourceInfo(source_id=bid,source_name=boardName,source_desc=boardDesc,site_id=19)
        return DocumentList(source_info=si,doc_list=threadList)

        #return {"boardName":boardName,"boardDesc":boardDesc,"categoryName":categoryName,"cover":cover,"threadList":threadList}

if __name__ == "__main__":
    huatan = Huatan()

    result = huatan.getThreadList(2124418905)


    print  result["boardName"]
    print  result["boardDesc"]
    print  result["categoryName"]
    print  result["cover"]
    for item in result["threadList"]:
        print item['tid']+"\r\n"+item["subject"] +"====="+item["content"]+"======="+item["created_at"]+"======="+item["url"]