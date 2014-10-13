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
            self.cj.revert('jsnh.cookie')
        except Exception,e:
            print e
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        urllib2.install_opener(self.opener)

    def setinfo(self,username,password):
        '''设置用户登录信息'''
        self.name = username
        self.pwd = password

    def login(self):
        '''登录jsnh  
      fastloginfield	username
		handlekey	ls
		password	wangzhuo1987
		quickforward	yes
		username	247970981
		http://www.jsnh.info/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1
		http://162.212.180.183/member.php?mod=logging&action=login&loginsubmit=yes&loginhash=LFdJ1&inajax=1'''
        params = {'username':self.name, 'password':self.pwd,'fastloginfield':'username','handlekey':'ls','quickforward':'yes'}
        print 'login.......'
        req = urllib2.Request(
            'http://www.jsnh.info/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1',
            urllib.urlencode(params)
        )
        self.operate = self.opener.open(req)
        #print self.operate.geturl()
         
        rawdata = self.operate.read()
        rawdata = rawdata.decode(chardet.detect(rawdata)['encoding'])
        print rawdata
        if rawdata.find("登录失败，你还可以尝试") < 0 :
            print 'Logged on successfully!'
            self.cj.save('jsnh.cookie')
            self.sign()
        else:
            print 'Logged on error'
    def sign(self):
        '''找到最新的领取MB的地址'''
        siteurl="http://www.jsnh.info/forum.php?mod=forumdisplay&fid=36"
        isfind = False
        count = 0
        while(isfind == False and count<=300):
            count = count + 1
            print '尝试次数'+str(count)
            req = urllib2.Request(siteurl)
            self.operate = self.opener.open(req)
            rawdata = self.operate.read()
            rawdata = rawdata.decode(chardet.detect(rawdata)['encoding'])
            #print rawdata
            #rawdata = rawdata.decode("gbk")
            for m in BeautifulSoup(rawdata).findAll(attrs={'class' : re.compile("new")}):
                e = m.find(attrs={'class' : re.compile("s xst")})
                if(e!=None):
                    print e
                    pattern = str(time.localtime()[0])+".*"+str(time.localtime()[1]) +".*"+ str(time.localtime()[2])
                    print pattern
                    time.sleep(1)
                    if(len(re.findall(pattern,str(e)))>0):
                        realUrl = e.get('href')
                        isfind = True
                        break
                    else:
                        time.sleep(0.2)
            else:
                continue
        print realUrl
        self.replyAndFetch("http://www.jsnh.info/" + realUrl)
    def replyAndFetch(self,realUrl):
        '''回复信息'''
        req = urllib2.Request(realUrl)
        self.operate = self.opener.open(req)
        rawdata = self.operate.read()
        rawdata = rawdata.decode(chardet.detect(rawdata)['encoding'])
        #rawdata = rawdata.decode('gbk')
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
        form_action = 'http://www.jsnh.info/'+form_action+'&inajax=1'
        print form_action
        #回复信息
        params = {'message':'shao xiang bao you ping an ~', 'formhash':formhash,'subject':'','usesig':''}
        print 'reply.......'
        req = urllib2.Request(
            form_action,
            urllib.urlencode(params)
        )
        self.operate = self.opener.open(req)
        rawdata = self.operate.read()
        print rawdata
moofeel = Moofeel()
import mypasswd
moofeel.setinfo(mypasswd.JSNH_USERNAME,mypasswd.JSNH_PASSWD)
moofeel.login()
