# coding=utf-8

# import httplib

from httplib2 import Http
import urllib
from django.utils import simplejson as json

if __name__ == "__main__":
    content = """
        逆境中成长，绝地里求生，不屈不饶，才能堪破武之极道。
    凌霄阁试炼弟子兼扫地小厮杨开偶获一本无字黑书，从此踏上漫漫武道。
    ******************
    感谢书友那不是爱、是依赖提供的打油诗一首：
　　武之巅峰，是孤独，是寂寞，是漫漫求索，是高处不胜寒    先天不足难修武，不屈之魂开黑书。
    金身岂可无傲骨，武道怎能有坦途。
    漫漫长路纵然苦，凌云壮志不屈服。
    荆棘遍布巅峰路，一将功成万骨枯。
    *****************
    """
    # params = urllib.urlencode({'datas':[{'uid': 12524, 'userName': '杨广钊◎123', 'title': '历史说《大宋私生子》',
    #                            'content': content,'date': '2013-05-07 18:09',
    #                            'cid': 0,'refSiteId': 1,'refId': 123456,'refUrl':'http://19lou.com/'},
    #                             {'uid': 7890, 'userName': '天天快乐◎123', 'title': '历史说1111《大宋私生子》',
    #                            'content': content,'date': '2013-05-07 18:09',
    #                            'cid': 0,'refSiteId': 1,'refId': 123456,'refUrl':'http://19lou.com/'}
    #                             ]})

    params = json.dumps({'datas':[{'uid': 12524, 'userName': '杨广钊◎123', 'title': '历史说《大宋私生子》',
                               'content': content,'date': '2013-05-07 18:09',
                               'cid': 0,'refSiteId': 1,'refId': 123456,'refUrl':'http://19lou.com/'},
                                {'uid': 7890, 'userName': '天天快乐◎123', 'title': '历史说1111《大宋私生子》',
                               'content': content,'date': '2013-05-07 18:09',
                               'cid': 0,'refSiteId': 1,'refId': 123456,'refUrl':'http://19lou.com/'}
                                ]})

    headers = {"Content-type": "application/json", "Accept": "text/plain","User-Agent": "Magic Browser"}
    h = Http()
    resp, content = h.request("http://127.0.0.1:8000/cron/add", "POST",body=params,headers=headers)
    print resp
