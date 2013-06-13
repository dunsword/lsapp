# coding=utf-8

REPLY_SUBSCRIBE='''欢迎关注精品阅读，每天为您同步推荐最热门的小说。回复“今天”查看今天的推荐内容，要查看一月内任一天的推荐，可回复日期，如要查看5月19日推荐，回复“519“就可以了。你也可以回复红太狼、小白、清新的竹、苹果等，看达人的推荐。你也回复查看高干、腹黑等内容。另外如果没有明确需求，可回复“随意”，查看随机推荐内容。'''

AUTHORS={'红太郎':14693355,
         '19楼红太郎':14693355,
         'CJ的小白':22545551,
         '小白':22545551
}

KEYWORDS=(
    '腹黑','高干','言情'
)

def get_response(msg):
    if AUTHORS.has_key(msg):
        return resp_from_author(msg)
    elif  KEYWORDS.__contains__(msg):
        return resp_from_keyword(msg)

def resp_from_keyword(msg):
    return 'keyword:'+msg

def resp_from_author(msg):
    pass


if __name__=='__main__':
    resp=get_response('腹黑')
    print resp