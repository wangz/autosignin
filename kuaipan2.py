__author__ = 'clownfish'
#coding:utf-8
import urllib2,urllib,cookielib,json
username = "快盘用户名"
password = "快盘密码"
class sign(object):
    username = ''
    password = ''
    #登录显示页面
    indexurl = 'https://www.kuaipan.cn/account_login.htm'
    #登录的form表单url
    loginurl = 'https://www.kuaipan.cn/index.php?ac=account&op=login'
    #签到的真正url
    signurl = 'http://www.kuaipan.cn/index.php?ac=common&op=usersign'
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def login(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        print "打开登录页面"
        try:
            urllib2.urlopen(self.indexurl)
            post_data = {'username':self.username,'userpwd':self.password,'isajax':'yes'}
            req=urllib2.Request(self.loginurl,urllib.urlencode(post_data))
        except Exception, e:
            print "网络链接错误"
            return False
        response = urllib2.urlopen(req)
        login=response.read()
        print login
        l = json.loads(login)
        if (l['state'] == 1):
            print "登录成功,准备签到！"
            return True
        else:
            print "登录失败！code:" +  str(l['errcode'])
            return False
        

    def sign(self):
        response = urllib2.urlopen(self.signurl)
        sign = response.read()
        print sign
        l = json.loads(sign)
        if (l and l['state'] == 1) or \
        (l and 0 == l['state'] and l['increase'] * 1 == 0 and l['monthtask'].M900 == 900):
            print "恭喜你签到成功！"
            k = l['increase']*1
            m = l['rewardsize'] * 1
            if (k == 0 and l['monthtask'].M900 == 900):
                print "本月签到积分已领取完成"
            else:
                print "签到奖励积分:%s" % (k)
            if m == 0:
                print "手气太不好了！奖励 0M 空间"
            else:
                print "签到奖励空间：%s" % (m)
        else:
            if (l['state'] == -102):
                print "今天您已经签到过了"
            else:
                print "签到失败，遇到网络错误，请稍后再试！"
        return sign

import mypasswd
if __name__ == "__main__": 
    sign = sign(mypasswd.KUAIPAN_USERNAME,mypasswd.KUAIPAN_PASSWD)
    if sign.login():
        sign.sign()
