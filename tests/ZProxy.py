import sys
sys.path.append("..")

from ztool import Http

pro = Http.ZProxy()
print pro.getIp()

