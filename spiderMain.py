# -- coding:utf-8 --
import threading
import requests
import time
from queue import Queue
from bs4 import BeautifulSoup
threads = []
start = time.time()
import urllib
deep=2 #控制爬行深度
global domain
# 建立队列，存储爬取网址
que = Queue(100000)
# 线程类，每个子线程调用，继承Thread类并重写run函数，以便执行我们的爬虫函数
proxy = ""
lock = threading.Lock()
file = open('srcaptest.txt', 'a+')
oldurl=[]
threadsNum = 2
class myThread(threading.Thread):
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


#返回url
def download(url):
    res=requests.get(url,timeout=3)
    return res.content

def doqueput(urls,que):
    for  newurl in urls:
        if IsSpidered(newurl) and IsOverDeep(newurl):
            print("checked，新url，没错")
            que.put(newurl)
            oldurl.append(newurl)
            print("已经爬取"+str(len(oldurl))+"条连接")
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

def crawler(que):
    with lock:
        baseurl = que.get(timeout=3)
        content = download(baseurl)
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

def IsSpidered(url):
    if url in oldurl:
        return False
    else:
        return True
    return True
def isinnerurl(url):
    urldata=urllib.parse.urlsplit(url)
    if domain==urldata[1]:
        return True
    else:
        return False
    return True

def urlclean(url):
    pass



def IsOverDeep(url):
    urldata=urllib.parse.urlsplit(url)
    SplitResult=str(urldata[2]).split('/')
    spiderdeep=len(SplitResult)-1
    print(len(SplitResult)-1)
    print("目前爬行深度："+str(spiderdeep))
    if  spiderdeep>=deep:
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

def Main():
    global domain
    url = 'http://www.freebuf.com'
    domain=getdomain(url)
    que.put(url)
    for i in range(threadsNum):
        thread = myThread(que)
        thread.start()
        threads.append(thread)
    # 同步线程，避免主线程提前终止，保证整个计时工作
    for t in threads:
        t.join()
    end = time.time()
    # 输出时间并结束
    print("The total time is:", end - start)

if __name__ == '__main__':
    Main()
