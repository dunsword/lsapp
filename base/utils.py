#coding=utf-8
__author__ = 'paul'

def is_cn_char(i):
    return 0x4e00<=ord(i)<0x9fa6
def is_cn_or_en(i):
    o = ord(i)
    return o<128 or 0x4e00<=o<0x9fa6
def is_legal(i):
    o=ord(i)

    return 97<=o<=122 or 65<=o<=90 or 0x4e00<=o<0x9fa6 or 48<=o<58 or o==95


if __name__ == "__main__":
    print is_legal(u'a')
    print is_legal(u'z')
    print is_legal(u'A')
    print is_legal(u'Z')
    print is_legal(u'@')
    print is_legal(u'_')
    print is_legal(u'0')
    print is_legal(u'9')