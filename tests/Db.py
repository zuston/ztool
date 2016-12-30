#!coding:utf-8
import sys
sys.path.append("..")

from ztool import Db

dbInstance = Db.Db(host='localhost',user='root',password='zuston',dbname='todo')
print dbInstance
print dbInstance.getOne('user','where id=2')
print dbInstance.execute('select  * from user where id = 2')
