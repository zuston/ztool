#!coding:utf-8
import sys
sys.path.append("..")

from ztool import ZMail
from ztool import DbConfig

print DbConfig.dbname
from ztool import MailConfig
print MailConfig.mailAccount
zmail = ZMail.ZMail()
zmail.setSendAddr('mailAddr')
zmail.sendMail('你好吗,很想你',From='zuston',To='ziusto',Subject='ad',File='./const.py')