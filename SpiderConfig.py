# -- coding:utf-8 --
from queue import Queue
import time
'''
配置队列大小
配置爬行深度
配置域名
配置线程数
'''

'''
        self.que=que

        self.deep=deep

        self.domain=domain

        self.threadsNum=threadsNum
'''
class SpiderConfig:

    def __init__(self):
        self.que='' #队列长度

        self.deep='' #爬行深度

        self.domain='' #域名

        self.threadsNum='' #线程数

        self.oldurl=[] #已爬取的url

        self.starttime=time.time() #开始时间

        self.finishedtime='' #结束时间

        self.threadspool=[]

    def addthread(self,thread):
        self.threadspool.append(thread)

    def setfinishedtime(self,finishedtime):
        self.finishedtime=finishedtime

    def setque(self,quesize):
        que=Queue(quesize)
        self.que=que

    def setoldurl(self,newurl):
        self.oldurl.append(newurl)

    def setdeep(self,deep):
        self.deep=deep

    def setdomain(self,domain):
        self.domain=domain

    def setthreadsNum(self,threadsNum):
        self.threadsNum=threadsNum

    def getthreadspool(self):
        return self.threadspool

    def getfinishedtime(self):
        return self.finishedtime

    def getque(self):
        return self.que

    def getdeep(self):
        return self.deep

    def getoldurl(self):
        return self.oldurl

    def getdomain(self):
        return self.domain

    def getthreadsNum(self):
        return self.threadsNum


