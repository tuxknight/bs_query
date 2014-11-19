#!/bin/python
#coding=utf8
import httplib
import urllib2
import time
from bae.core.wsgi import WSGIApplication
from sgmllib import SGMLParser
from HTMLParser import HTMLParser
from string import strip
from cgi import parse_qs, escape

#fetch http://www.hairongyi.com/
HOST = "www.hairongyi.com"
URL = "/"
#params = urllib.urlencode({"apiVersion":"2.0.0","appVersion":"2.0.1","deviceOp":"4.4.4","deviceOs":"Android","deviceType":"Meizu%2CM353","netType":"WIFI","picErrNum":"0","positionTag":"%7B%22state%22%3A%22%5Cu6c5f%5Cu82cf%5Cu7701%22%2C%22city%22%3A%22%5Cu82cf%5Cu5dde%5Cu5e02%22%7D","uId":"163fee650a45d21179ed083f"})
headers = {"Content-type":"application/x-www-form-urlencoded","User_Agent":"User-Agent: Dalvik/1.6.0 (Linux; U; Android 4.4.2; C6903 Build/14.3.A.0.681)","Connection":"Keep-Alive","Accept-Encoding":"gzip"}
#print "POST "+HOST+URL+"\n"+params
print "GET "+HOST+URL
conn = httplib.HTTPConnection(HOST) 
#conn.request("post",URL,params,headers)
conn.request("get",URL,"",headers)
print "response"
response = conn.getresponse()
print "receive"
data = response.read()
#print response.status, response.reason
#print data
conn.close()

class MyHTMLParser(SGMLParser):
    def __init__(self, verbose = 0):
        SGMLParser.__init__(self)
        self.hry_tradeInfo = []
        self.hry_fund = []
        self.flag_div = False
        self.flag_ul = False
        self.flag_li = False
        self.flag_span = False
        self.flag_rate = False
        self.is_span = False
    def start_div(self,attrs):
        for k,v in attrs:
            if k == "class":
                if v == "hry_fund_counts" or v == "hry_tradeInfo" or v == "hry_fund_fundnav":
                    self.flag_div = True
                else:
                    self.flag_div = False
    def end_div(self):
        self.flag_div = False
    def start_ul(self,attrs):
        for k,v in attrs:
            if k == "class":
                if v == "hry_tradeInfo_list":
                    self.flag_ul = True
                else:
                    self.flag_ul = False
    def end_ul(self):
        self.flag_ul = False    
    def start_li(self,attrs):
        for k,v in attrs:
            if k == "class":
                if v == "hry_inline_block":
                    self.flag_li = True
                else:
                    self.flag_li = False  
    def end_li(self):
        self.flag_li = False
    def start_span(self,attrs):
        self.is_span = True
        if self.flag_ul and self.flag_li:
            self.flag_span = True
        else:
            self.flag_span = False
    def end_span(self):
        self.is_span = False
        self.flag_span = False
        self.flag_rate = False
    def handle_data(self,data):
        
        #处理<div><ul><li><span></span></li><ul/></div>
        #单日交易金额  累计交易金额  当前在线人数
        if self.flag_ul and self.flag_li and self.flag_span:
            result=strip(data)
            l = len(self.hry_tradeInfo)
            self.hry_tradeInfo.insert(l,result)
        if self.flag_div and self.is_span:
            result=strip(data)
            l = len(self.hry_fund)
            self.hry_fund.insert(l,result)

def app(environ, start_response):
    dic = {'3':'Sucessed','4':'Failed','5':'Timeout'}
    qs = parse_qs(environ['QUERY_STRING'])
    crontab_callback_URL= qs.get('URL',[''])[0]
    crontab_callback_code= qs.get('reason',[''])[0]
    callback = dic[crontab_callback_code]
    parser = MyHTMLParser()
    parser.feed(data)
    trade_count_today = parser.hry_tradeInfo[0]
    trade_count_total = parser.hry_tradeInfo[1]
    online_count = parser.hry_tradeInfo[2]
    fund_7 = parser.hry_fund[0]
    fund_m = parser.hry_fund[1]
    online_count = parser.hry_fund[2]
    query_timestamp = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
    info1 = ','.join(parser.hry_tradeInfo)
    info2 = ','.join(parser.hry_fund)
    info = query_timestamp+','+info1+','+info2+'\n'
    file_csv=file("hry.csv","a")
    file_csv.write(info)
    file_csv.close()
    #print info
    #time.sleep(5)
    status = "200 OK"
    response_body=info
    response_header = [('Content-type', 'text/html'),('Content-Length',str(len(response_body)))]
    start_response(status, response_header)
    return response_body

application = WSGIApplication(app)
