# -- coding:utf-8 --
import threading
import requests
import time
from queue import Queue
from bs4 import BeautifulSoup
import urllib
from SpiderConfig import SpiderConfig

#线程锁
lock = threading.Lock()
spiderconf = SpiderConfig()

'''
Mutiple Threads SuperSpider
'''
class SuperSpider(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.que = que

    def run(self):
        print("Start--a threads")
        while True:
            #try:
                crawler(self.que)
            #except:
             #   break
        print("Exiting One Threads")


#下载页面内容
def download(url):
    flag=True
    while(flag):
        try:
            if spiderconf.getproxystatus():#判断是否启用了代理
                res=requests.get(url,timeout=4,proxies=spiderconf.getproxy())
                flag=False
            else:
                res=requests.get(url,timeout=4)
                flag=False
                #要智能点，可以在这里加一个403判断，如果status_code是403则启用代理
        except:
            spiderconf.setproxy(getproxy())#切换代理
    return res

#往队列里添加url
def doqueput(urls,que):
    for  newurl in urls:
        if IsSpidered(newurl) and IsOverDeep(newurl):
            if newurl.endswith('xml') or newurl.endswith('pom'):
                res=download(newurl)
                spiderconf.getsavefile().write(newurl + "\n")
                spiderconf.getsavefile().write(res.text + "\n")
        if IsSpidered(newurl) and IsOverDeep(newurl):
            #print("checked，新url，没错")
            que.put(newurl)
            spiderconf.oldurl.append(newurl)
            print("已经爬取"+str(len(spiderconf.oldurl))+"条连接")
            print("将新url放到que中：" + newurl)
            print("队列大小:"+str(que.qsize()))

# 解析url，放入队列
def parseURL(que, urls):
        doqueput(urls,que)

def getdomain(url):
    domain=urllib.parse.urlsplit(url)[1]
    return domain

# 爬虫主程序
#url解析策略目前只提取判断a中的全路径的url
'''
                       else:
                           if '../' not in url:
                               url=baseurl+url
                               newurls.append(url)
'''
def crawler(que):
    with lock:
            baseurl = que.get(timeout=3)
            content = download(baseurl).content
            soup = BeautifulSoup(content, 'html.parser')
            AllHrefTag = soup.find_all('a')
            newurls = []
            for hreftag in AllHrefTag:
                 try:
                       url = str(hreftag['href'])
                       if "http:" in url and isinnerurl(url):
                           newurls.append(url)
                       elif "https:" in url and isinnerurl(url):
                           newurls.append(url)
                 except:
                   continue
            newurls=set(newurls)
            parseURL(que, newurls)

#判断是否是已经爬取
def IsSpidered(url):
    if url in spiderconf.oldurl:
        return False
    else:
        return True
    return True

#判断是否是当前域内的URL
def isinnerurl(url):
    urldata=urllib.parse.urlsplit(url)
    if spiderconf.getdomain()==urldata[1]:
        return True
    else:
        return False
    return True

#URL净化
def urlclean(url):
    pass

'''
判断是否超过设定的爬行深度
'''
def IsOverDeep(url):
    urldata=urllib.parse.urlsplit(url)
    SplitResult=str(urldata[2]).split('/')
    spiderdeep=len(SplitResult)-1
    #print("目前爬行深度："+str(spiderdeep))
    if  spiderdeep>=spiderconf.getdeep():
        return False
    else:
        return True
    return True

# 获取代理
def getproxy():
    flag = True
    ipdic = {'http': 'http://119.114.125.253:58424'}
    while (flag):
        try:
            res = requests.get('http://api.ip.data5u.com/dynamic/get.html?order=4a2c1091b15515eff96cadddf0228a16&sep=6',timeout=5)
            # res=requests.get('http://dps.kdlapi.com/api/getdps/?orderid=994460608536855&num=1&pt=1&ut=1&sep=4',timeout=3)
            ip = res.text.replace(";", "").replace("\n", "").replace("|", "")
            ipdic = {'http': 'http://' + ip}
            print(ipdic)
            flag = False
        except:
            continue
    return ipdic

'''
平衡线程池
'''
def BalanceThreadsPool(SpiderConfig):
    if len(SpiderConfig.getthreadspool())<SpiderConfig.getthreadsNum():
        addtionalThreadsNum=SpiderConfig.getthreadsNum()-len(SpiderConfig)
        for i in range(addtionalThreadsNum):
            thread = SuperSpider(spiderconf.getque())
            thread.setDaemon(True)
            thread.start()
            thread.join()
            spiderconf.addthread(thread)

def startspider():
    for i in range(spiderconf.getthreadsNum()):
        thread = SuperSpider(spiderconf.getque())
        thread.setDaemon(True)
        thread.start()
        spiderconf.addthread(thread)
    # 同步线程，避免主线程提前终止，保证整个计时工作
    for t in spiderconf.getthreadspool():
        t.join()

#爬虫主函数
def Main():
    url = 'http://www.freebuf.com'

    '''
    爬虫全局配置
    '''
    spiderconf.setdomain(getdomain(url))  #设置域名
    spiderconf.setdeep(100)                 #设置爬行深度
    spiderconf.setque(10000000)             #设置队列大小
    spiderconf.setthreadsNum(5)           #设置线程数量
    spiderconf.getque().put(url)          #将域名push到队列中
    spiderconf.setproxyswitch(False)       #打开/关闭代理，默认是关闭
    spiderconf.setproxy(getproxy())       #设置代理
    startspider()                         #开始扫描
    spiderconf.setfinishedtime(time.time())

    # 输出时间并结束
    print("The total time is:", spiderconf.getfinishedtime() - spiderconf.starttime)

if __name__ == '__main__':
    Main()
