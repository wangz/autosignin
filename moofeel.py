#!/usr/bin/python
#encoding=utf-8
import sys,re,urllib2,urllib,cookielib,chardet,time
from BeautifulSoup import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf8')
# by wangz
class Moofeel(object):
    def __init__(self):
        self.name = self.pwd = self.content = ''
        self.cj = cookielib.LWPCookieJar()
        try:
            self.cj.revert('moofeel.cookie')
        except Exception,e:
            print e
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def setinfo(self,username,password):
        '''设置用户登录信息'''
        self.name = username
        self.pwd = password

    def login(self):
        '''登录moofeel'''
        params = {'username':self.name, 'password':self.pwd}
        print 'login.......'
        req = urllib2.Request(
            'http://www.moofeel.com/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes',
            urllib.urlencode(params)
        )
        self.operate = self.opener.open(req)
        #print self.operate.geturl()
        rawdata = self.operate.read()
        rawdata = rawdata.decode(chardet.detect(rawdata)['encoding'])
        if rawdata.find("登录失败，你还可以尝试") < 0 :
            print 'Logged on successfully!'
            self.cj.save('moofeel.cookie')
            self.sign()
        else:
            print 'Logged on error'
    def sign(self):
        '''找到最新的领取MB的地址'''
        siteurl="http://www.moofeel.com/forum-96-1.html"
        isfind = False
        count = 0
        while(isfind == False):
            count = count + 1
            print '尝试次数'+str(count)
            req = urllib2.Request(siteurl)
            self.operate = self.opener.open(req)
            rawdata = self.operate.read()
            rawdata = rawdata.decode(chardet.detect(rawdata)['encoding'])
            for m in BeautifulSoup(rawdata).findAll(attrs={'class' : re.compile("new")}):
                e = m.find(attrs={'class' : re.compile("xst")})
            if(e!=None):
                pattern = str(time.localtime()[0])+".*"+str(time.localtime()[1]) +".*"+ str(time.localtime()[2])
                if(len(re.findall(pattern,str(e)))>0):
                    realUrl = e.get('href')
                    isfind = True
                else:
                    time.sleep(0.2)
            else:
                continue
        print realUrl
        self.replyAndFetch(realUrl)
    def replyAndFetch(self,realUrl):
        '''回复信息并领取MB'''
        req = urllib2.Request(realUrl)
        self.operate = self.opener.open(req)
        rawdata = self.operate.read()
        #rawdata = rawdata.decode(chardet.detect(rawdata)['encoding'])
        rawdata = rawdata.decode('gbk')
        #获取formhash
        formhash = None
        for m in BeautifulSoup(rawdata).findAll('input'):
            if(m.get('name')=='formhash'):
                formhash = m.get('value')
        print formhash   
        #获取form action
        form_action = None     
        for m in BeautifulSoup(rawdata).findAll('form'):
            if(m.get('id')=='fastpostform'):
                form_action = m.get('action')
        print form_action
        #获取领取MB地址
        fetchmb_url = None
        for m in BeautifulSoup(rawdata).findAll('a'):
            for x in m.findAll('img'):
                if(x.get('src').find('signin_reply')>0):
                    fetchmb_url = m.get('href')
        print "fetchmb_url" + str(fetchmb_url)
        #回复信息
        params = {'message':'I like this ~', 'formhash':formhash,'subject':''}
        print 'reply.......'
        req = urllib2.Request(
            'http://www.moofeel.com/'+form_action,
            urllib.urlencode(params)
        )
        self.operate = self.opener.open(req)
        rawdata = self.operate.read()
        #点击领取MB
        self.operate = urllib2.urlopen(fetchmb_url)
        rawdata = self.operate.read()
        print rawdata.decode('gbk')
moofeel = Moofeel()
username = 'nightfight'#你的moofeel网的帐号
password = 'nightfight'#你的moofeel网的密码

import mypasswd
moofeel.setinfo(mypasswd.MOOFEEL_USERNAME,mypasswd.MOOFEEL_PASSWD)
moofeel.login()
