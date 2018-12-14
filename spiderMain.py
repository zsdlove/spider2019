# -- coding:utf-8 --
import threading
import requests
import time
from queue import Queue
from bs4 import BeautifulSoup
threads = []
start = time.time()
import urllib

global domain
# 建立队列，存储爬取网址
que = Queue(100000)
# 线程类，每个子线程调用，继承Thread类并重写run函数，以便执行我们的爬虫函数
global cout
cout = 0
proxy = ""
lock = threading.Lock()
file = open('srcaptest.txt', 'a+')
oldurl=[]

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
    return res

def doqueput(urls,que):
    for  newurl in urls:
        if IsSpidered(newurl):
            print("checked，新url，没错")
            que.put(newurl)
            oldurl.append(newurl)
            print("已经爬取"+str(len(oldurl))+"条连接")
            print("将新url放到que中：" + newurl)
            print("队列大小:"+str(que.qsize()))
# 解析url，放入队列
def parseURL(que, urls):
        #res = download(newurl)
        doqueput(urls,que)

def getdomain(url):
    domain=urllib.parse.urlsplit(url)[1]
    return domain

# 爬虫主程序
#url解析策略目前只提取判断a中的全路径的url

def crawler(que):
    with lock:
        e=threading.Event()
        if que.qsize==0:
            e.wait()
        baseurl = que.get(timeout=3)
        print(baseurl)
        #try:
        response = requests.get(baseurl, timeout=4)
        #except:
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        AllHrefTag = soup.find_all('a')
        newurls = []
        for hreftag in AllHrefTag:
             #try:
               url = str(hreftag['href'])
               if "http://" in url and isinnerurl(url):
                   newurls.append(url)
                   global cout
                   cout=cout+1
             #except:
              # continue
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

if __name__ == '__main__':
    global domain
    url = 'http://www.freebuf.com'
    domain=getdomain(url)
    que.put(url)
    for i in range(1, 10):
        thread = myThread(que)
        thread.start()
        threads.append(thread)
    # 同步线程，避免主线程提前终止，保证整个计时工作
    for t in threads:
        t.join()
    end = time.time()
    # 输出时间并结束
    print("The total time is:", end - start)
