#!coding:utf-8

import redis

import ztool.config.DbConfig as config

class ZQueue(object):
    def __init__(self):
        self.redisConn = redis.StrictRedis(host=config.redisDict['host'], port=config.redisDict['port'])
        self.containerName = None

    def setContainerName(self,name):
        self.containerName = name

    def push(self,value):
        self.redisConn.lpush(self.containerName,value)

    def pop(self):
        return self.redisConn.lpop(self.containerName)

    def isEmpty(self):
        return self.redisConn.llen(self.containerName)==0

    def len(self):
        return self.redisConn.llen(self.containerName)

    def flush(self):
        self.redisConn.delete(self.containerName)

if __name__ == '__main__':
    zr = ZQueue()
    print zr.pop()
    print zr.redisConn.llen(zr.containerName)