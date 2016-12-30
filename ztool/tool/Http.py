# -*- coding:utf-8 -*-
import urllib2
import urllib
import gzip
from StringIO import StringIO
import sys
import time
import redis
from bs4 import BeautifulSoup as bs
import ztool.config.DbConfig as config
reload(sys)
sys.setdefaultencoding("utf8")


class Http(object):

    def __init__(self):
        self.proxyFlag = False


    def costTimeDec(func):
        def wrapper(*args,**kw):
            startTime = time.time()
            res = func(*args,**kw)
            endtime = time.time()
            costTime = endtime-startTime
            print 'the spider process cost is:',costTime
            return res
        return wrapper

    # @costTimeDec
    def _request(self,url,postValue=None,**headers):
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36';
        if not headers:
            headers = {'User-Agent': user_agent}
        else:
            if 'User-Agent' not in headers:
                headers['User-Agent'] = user_agent
        if postValue is not None:
            postData = urllib.urlencode(postValue)
            request = urllib2.Request(url, postData, headers)
        else:
            request = urllib2.Request(url,headers=headers)

        if self.proxyFlag:
            # need to spider the proxyIp
            proxyIp = self._getProxyIp()
            print proxyIp
            proxy_handler = urllib2.ProxyHandler({'http':proxyIp})
            urllib2.install_opener(urllib2.build_opener(proxy_handler))

        try:
            response = urllib2.urlopen(request,timeout=10)
            code = response.getcode()
            resMsg = response.msg
            pageEncoding = response.info().get('Content-Encoding')
            page = response.read()
            if pageEncoding == 'gzip':
                buf = StringIO(page)
                f = gzip.GzipFile(fileobj=buf)
                page = f.read()

            return [code,resMsg,page]
        except Exception as e:
            code = -2
            page = None
            return [code,e,page]

    def _getProxyIp(self):
        proxyInstance = ZProxy()
        ip = proxyInstance.getIp()
        return ip

    def post(self,url,postValue,**headers):
        return self._request(url,postValue,**headers)

    def open(self,url,**headers):
        return self._request(url,**headers)

    def openProxy(self):
        self.proxyFlag = True

    def closeProxy(self):
        self.proxyFlag = False




class ZProxy(object):
    def __init__(self):
        self.proxyName = config.redisDict['proxyName']
        self._getRedisConn()

    def _getRedisConn(self):
        self.redisConn = redis.StrictRedis(host=config.redisDict['host'], port=config.redisDict['port'])

    def _parseDate(self, html):
        ip_data = []
        soup = bs(html)
        group = soup.find_all("tr", class_="odd")
        for onedata in group:
            temp = []
            ip = (onedata.find_all("td"))[1].string
            port = (onedata.find_all("td"))[2].string
            # print "IP:%s\tPort:%s" % (ip, port)
            ip_data.append(ip + ":" + port)
        return ip_data

    def _getProxyIp2Pool(self):
        # 维持一个代理池，采用的是西祠的透明代理
        hp = Http()
        _headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Host": "www.xicidaili.com",
            "Referer": "http://www.xicidaili.com/nt/1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"
        }
        url = "http://www.xicidaili.com/nt/"

        code, msg, page = hp.open(url, **_headers)
        if code != 200:
            print "can not get the ip"
            return False

        resList = self._parseDate(page)
        for r in resList:
            self.redisConn.sadd(self.proxyName, r)
        return True

    def getIp(self):
        count = self.redisConn.scard(self.proxyName)
        if count <= 1 or count is None:
            self._getProxyIp2Pool()
            return self.getIp()
        else:
            proxyIP = self.redisConn.spop(self.proxyName)
            return proxyIP

    def flushPool(self):
        pass



# 代理挂载
if __name__ == '__main__':

    proxy = ZProxy()
    print proxy.getIp()