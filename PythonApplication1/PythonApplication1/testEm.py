#by 李星星
# -*- coding:utf-8 -*-

import urllib.request
import re
import http.cookiejar
import urllib.parse

#163邮箱类
class MAIL:

    #初始化
    def __init__(self):
        #获取登录请求的网址，这个是通用的，只是一个请求登陆的URL
        self.loginUrl = "https://mail.163.com/entry/cgi/ntesdoor?style=-1&df=mail163_letter&net=&language=-1&from=web&race=&iframe=1&product=mail163&funcid=loginone&passtype=1&allssl=true&url2=https://mail.163.com/errorpage/error163.htm"
        #设置代理，以防止本地IP被封
        self.proxyUrl = "http://202.106.16.36:3128"
        #初始化sid码
        self.sid = ""
        #第一次登陆所需要的请求头request headers,这些信息可以在ntesdoor日志request header中找到，copy过来就行
        self.loginHeaders = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,,image/webp,image/apng,*/*;q=0.8",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "mail.163.com",
            'Referer': "http://mail.163.com/",
            #'User-Agent':"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36"
            'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36 2345Explorer/9.9.0.19250"
        }
        #设置用户名和密码，填上自己的即可
        self.username = '17354422606@163.com'
        self.pwd = 'xing3239'
        #post所包含的参数
        self.post = {
            'savelogin':"0",
            'url2':"http://mail.163.com/errorpage/error163.htm",
            'username':self.username,
            'password':self.pwd
        }
        #对post编码转换
        self.postData = urllib.parse.urlencode(self.post).encode('utf8')
        # 使用http.cookiejar.CookieJar()创建CookieJar对象
        self.cjar = http.cookiejar.CookieJar()
        # 使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
        self.cookie = urllib.request.HTTPCookieProcessor(self.cjar)
        self.opener = urllib.request.build_opener(self.cookie)
        # 将opener安装为全局
        urllib.request.install_opener(self.opener)

    #模拟登陆并获取sid码
    def loginPage(self):
        try:
            #发出一个请求
            self.request = urllib.request.Request(self.loginUrl,self.postData,self.loginHeaders)
        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.read().decode("utf8"))
        #得到响应
        self.response = urllib.request.urlopen(self.request)
        #需要将响应中的内容用read读取出来获得网页代码，网页编码为utf-8
        self.content = self.response.read().decode("utf8")
        #打印获得的网页代码
        #print (self.content)
        # 设定提取sid码的正则表达式
        self.sidpattern = re.compile('sid=(.*?)&', re.S)
        self.result = re.search(self.sidpattern, self.content)
        self.sid = self.result.group(1)
        #print (self.sid)

    #通过sid码获得邮箱收件箱信息
    def messageList(self):
        #重定向至收件箱的网址
        receiveUrl =  'http://mail.163.com/js6/s?sid=%s&func=mbox:listMessages&TopTabReaderShow=1&TopTabLofterShow=1&welcome_welcomemodule_mailrecom_click=1&LeftNavfolder1Click=1&mbox_folder_enter=1'%self.sid
        
        #新的请求头
        Headers = {
            'Accept': "text/javascript",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "mail.163.com",
            'Referer': "https://mail.163.com/js6/main.jsp?sid=%suCFJZNnnRnInrsigqunnSrQXsvMMqctH&df=mail163_letter"%self.sid,  
            'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"
        }
        #发出请求并获得响应
        request = urllib.request.Request(receiveUrl, headers = Headers)
        response = self.opener.open(request)
        #提取响应的页面内容，里面是收件箱的信息
        content = response.read().decode('utf-8')
        #print('~~~')
        #print(content)
        return content

    #获取邮件信息
    def getmail(self):
        messages = self.messageList()
        
        #print(messages)

        with open("1",mode='w',encoding='utf-8') as file:
            file.write(messages)
  
        pattern = re.compile('from..(.*?),.*?to..(.*?),.*?subject..(.*?),.*?sentDate..(.*?),\n.*?receivedDate..(.*?),\n',re.S)
        p=re.compile('id..(.*?),', re.S)
        m=re.findall(p,messages)
        i = 0
        mails = re.findall(pattern, messages)
        #for mail in mails:
         #   print ('-'*50)
          #  print ('发件人:',mail[0],'主题:',mail[2],'发送时间:',mail[3])
           # print ('收件人:',mail[1],u'接收时间:',mail[4])
            #print('https://mail.163.com/js6/read/readhtml.jsp?mid='+ eval(m[i]) + '&userType=browser&font=15&color=064977')
            #i+=3
        
        receiveUrl =  'https://mail.163.com/js6/read/readhtml.jsp?mid=163:1tbiowbktVUMNCyuXAAAsH&userType=browser&font=15&color=064977'
        #新的请求头
        Headers = {
            'Accept': "text/javascript",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Connection': "keep-alive",
            'Host': "mail.163.com",
            'Referer': "https://mail.163.com/js6/main.jsp?sid=%s&df=mail163_letter"%self.sid,  
            'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"
        }
        request = urllib.request.Request(receiveUrl,headers = Headers)
        response = self.opener.open(request)
        content = response.read().decode('utf-8')
        print(content)
     
#创建163邮箱爬虫类
mail = MAIL()
mail.loginPage()
mail.getmail()

