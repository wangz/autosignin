#!/usr/bin/env python
#encoding=utf-8
import sys
import re
import urllib2
import urllib
import cookielib
import chardet

class Verypsp(object):
    
    def __init__(self):
        self.name = self.pwd = self.content = ''
        self.cj = cookielib.LWPCookieJar()
        try:
            self.cj.revert('verypsp.cookie')
        except Exception,e:
            print e
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def setinfo(self,username,password):
        '''设置用户登录信息'''
        self.name = username
        self.pwd = password
        
    def login(self):
        '''verypsp'''
        params = {'username':self.name, 'password':self.pwd}
        print 'login.......'
        req = urllib2.Request(
            'http://bbs.verypsp.com/logging.php?action=login&loginsubmit=yes',
            urllib.urlencode(params)
        )
        self.operate = self.opener.open(req)
        #print self.operate.geturl()
        rawdata = self.operate.read()
        #print chardet.detect(rawdata)['encoding']
        #rawdata = rawdata.decode(chardet.detect(rawdata)['encoding'])
        rawdata = rawdata.decode('gbk')
        print rawdata
        if rawdata.find("登录失败，您还可以尝试") < 0 :
            print 'Logged on successfully!'
            self.cj.save('moofeel.cookie')
            self.sign()
        else:
            print 'Logged on error'        
verypsp = Verypsp()
import mypasswd
verypsp.setinfo(mypasswd.VERYPSP_USERNAME,mypasswd.VERYPSP_PASSWD)
verypsp.login()
