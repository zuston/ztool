#!coding:utf-8
import sys
sys.path.append("..")

from ztool import Http

hp = Http.Http()
hp.closeProxy()
code,res,msg = hp.open("http://www.baidu.com")
print code,res