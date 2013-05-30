# coding=utf-8

import urllib
import sqlite3
from httplib2 import Http
from django.utils import simplejson as json

class WebPageContent:
    """ 根据url获得页面的内容用于数据分析 """
    def __init__(self,url):
        sock = urllib.urlopen(url)
        self.htmlSource = sock.read()
        sock.close()
    def getData(self):
        return self.htmlSource


if __name__ == "__main__":
    # conn = sqlite3.connect('/Users/yanggz/myPythonSpace/cron.db')
    # c = conn.cursor()
    # c.execute('''CREATE TABLE stocks
    #          (date text, trans text, symbol text, qty real, price real)''')
    # c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    # conn.commit()

    # symbol = 'IBM'
    # c.execute("SELECT * FROM stocks WHERE symbol = '%s'" % symbol)

    # Do this instead
    # t = ('IBM',)
    # c.execute('SELECT * FROM stocks WHERE symbol=?', t)
    # print c.fetchall()

    # Larger example that inserts many records at a time
    # purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
    #              ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
    #              ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
    #             ]
    # c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)
    # conn.commit()
    #
    # conn.close()
    params = json.dumps({'client_id': 100, 'client_secret': 'accessTest7118jqq54113accessTest', 'tid': 6061368972647982,
                               'authorUid': 10364894,'filterWater': 'true',
                               'page': 1,'perPage': 10}
                        )

    headers = {"Content-type": "application/json", "Accept": "text/plain","User-Agent": "Magic Browser"}
    h = Http()

    resp, content = h.request("https://www.19lou.com/api/thread/getThreadView", "POST",body=params,headers=headers)
    print resp
    print
    # a =json.loads(content)
    # for item in json.loads(content).get("datas"):
    #     print item.get("uid")
    #     print item.get("name")
    # print json.loads(content)




