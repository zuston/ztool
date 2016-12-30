# -*- coding:utf-8 -*-
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib
import sys
# 引入配置
from ztool.config import MailConfig as config
import os
'''
发送邮件的工具类
'''
class ZMail(object):
    def __init__(self):
        self.mailAccount = config.mailAccount
        self.mailPwd = config.mailPwd
        self.smtpServer = config.smtpServer
        self.popServer = config.popServer
        self.sendAddr = None

    def _format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr(( Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))


    def setSendAddr(self,sendAddr):
        self.sendAddr = sendAddr

    def sendMail(self,mailInfo,**attachmentConfig):
        # if attachmentConfig!=type(dict):
        #     raise Exception("please check the param")
        if not attachmentConfig.has_key('From'):    attachmentConfig['From'] = 'unknown'
        if not attachmentConfig.has_key('To'):    attachmentConfig['To'] = 'unknown'
        if not attachmentConfig.has_key('Subject'):    attachmentConfig['Subject'] = 'none'
        if not attachmentConfig.has_key('File'):    pass

        msg = MIMEMultipart()
        msg['From'] = self._format_addr(u'%s <%s>' %(attachmentConfig['From'],self.mailAccount))
        msg['To'] = self._format_addr(u'%s <%s>' %(attachmentConfig['To'],self.sendAddr))
        msg['Subject'] = Header(u'%s'%attachmentConfig['Subject'], 'utf-8').encode()
        # 发送内容
        msg.attach(MIMEText(mailInfo,'plain','utf-8'))
        if attachmentConfig.has_key('File'):
            attachmentPath = attachmentConfig['File']
            fileSuffix = os.path.basename(attachmentPath).split('.')[-1]
            print fileSuffix
            with open(attachmentPath,'rb') as file:
                mime = MIMEBase(fileSuffix,fileSuffix,filename='leetcode.'+fileSuffix)
                mime.add_header('Content-Disposition', 'attachment', filename='leetcode.'+fileSuffix)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                mime.set_payload(file.read())
                encoders.encode_base64(mime)
                msg.attach(mime)

        server = smtplib.SMTP(self.smtpServer, 25)  # SMTP协议默认端口是25
        server.set_debuglevel(0)
        server.login(self.mailAccount, self.mailPwd)
        server.sendmail(self.mailAccount, self.sendAddr, msg.as_string())
        server.quit()


    def getMail(self):
        pass



