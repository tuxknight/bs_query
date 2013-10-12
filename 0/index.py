#-*- coding:utf-8 -*-
from  wri_bsid_search import *
#BSID = '3610000E1103'
#BSID = '3610000E0092'
#BSID = '46000185DE122'
#BSID = '46001A8042A01'
reload(sys)
sys.setdefaultencoding('utf-8')
list = ('3610000E1103','46000185DE122','3610000E0092','46001A8042A01')
c = 0
head = ('BSID','经度','纬度','基站描述','覆盖半径')
body = ''
for i in list:
    if c == 0:
        #print '\t'.join(head).encode('gb2312')
        body='\t'.join(head).encode('gb2312')
    c = c+1
    bs1 = Bs(i)
    result = bs1.resultSet()
    body = body + '</br>' + result.encode('gb2312')

def app(environ, start_response):
	status = '200 OK'
	headers = [('Content-type', 'text/html')]
	start_response(status, headers)
	#body=["Welcome to Baidu Cloud!\n"]
	return body
application = WSGIApplication(app)
