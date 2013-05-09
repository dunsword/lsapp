# encoding=utf-8
'''
Created on 2013-5-7

@author: paul
'''

from sae.mail import EmailMessage

class MailClient:
    def __init__(self,smtp):
        """
        smtp=("smtp.vampire.com", 25, "damon@vampire.com", "password", False)
             (smtp主机，smtp端口， 用户名，密码，是否启用TLS）
        
        """
        self.__smtp=smtp
        
    def sentMail(self,to,subject,html):
        m = EmailMessage()
        m.to = to
        m.subject = subject
        m.html = html
        m.smtp = self.__smtp
        m.send()

smtp1=("smtp.163.com",25,"tuiadmin@163.com","tuitui2",False)

SentMail=MailClient(smtp1)