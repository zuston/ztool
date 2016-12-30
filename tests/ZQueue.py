import sys
sys.path.append("..")

from ztool import ZQueue

zr = ZQueue.ZQueue()
zr.setContainerName("tests")
print zr.push("zuston")
print zr.pop()
print zr.redisConn.llen(zr.containerName)