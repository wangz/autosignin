#!/usr/bin/env python
#encoding=utf-8
import sys
import re
import urllib2
import urllib
import cookielib
import chardet

reload(sys) 
sys.setdefaultencoding('utf-8')

class Kuaipan(object):
    
    def __init__(self):
        self.name = self.pwd = self.content = ''
        self.cj = cookielib.LWPCookieJar()
        try:
            self.cj.revert('kuaipan.cookie')
        except Exception,e:
            print e
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def setinfo(self,username,password):
        '''设置用户登录信息'''
        self.name = username
        self.pwd = password
        
    def login(self):
        '''kuaipan login'''
        params = {'username':self.name, 'userpwd':self.pwd,'isajax':'yes'}
        print 'login.......'
        user_agent ='Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130514 Firefox/17.0'
        headers = { 'User-Agent' : user_agent }
        
        req = urllib2.Request(
            'https://www.kuaipan.cn/index.php?ac=account&op=login',
            urllib.urlencode(params),
            headers
        )
        self.operate = self.opener.open(req)
        #print self.operate.geturl()
        rawdata = self.operate.read()
        #print chardet.detect(rawdata)['encoding']
        #rawdata = rawdata.decode(chardet.detect(rawdata)['encoding'])
        rawdata = rawdata.decode('utf8')
        print rawdata
        if rawdata.find("登录失败，您还可以尝试") < 0 :
            print 'Logged on successfully!'
            self.cj.save('kuaipan.cookie')
            #self.getindex()
        else:
            print 'Logged on error'    
            
    def getindex(self):
        '''get index'''
        req = urllib2.Request("http://www.kuaipan.cn/index.php?ac=home&op=dir&withdel=0&fileId=0")
        self.operate = self.opener.open(req)
        rawdata = self.operate.read()     
        print rawdata   
kuaipan = Kuaipan()
import mypasswd
kuaipan.setinfo(mypasswd.KUAIPAN_USERNAME,mypasswd.KUAIPAN_PASSWD)
kuaipan.login()
