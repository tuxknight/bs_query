#-*- coding:utf-8 -*-
from bae.core.wsgi import WSGIApplication
from  wri_bsid_search import *
from cgi import parse_qs, escape
import sys
import hashlib
import logging
#import markdown
reload(sys)
sys.setdefaultencoding('utf-8')
TOKEN = "chufuyuan0420"
logging.basicConfig(level=logging.DEBUG,
	format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
	datefmt='%a, %d %b %Y %H:%M:%S',
	filename='/home/bae/log/mp_wx.log',
	filemode='w')
def check_signature(sig,stamp,nonc,tk):
    par = [tk,stamp,nonc]
    parstr = "".join(sorted(par))
    tmpstr = hashlib.sha1(parstr).hexdigest()
    if tmpstr == sig:
	return True
    else:
	return False

def app(environ, start_response):
    status = "200 OK"
    #解析 HTTP GET 的参数
    d = parse_qs(environ["QUERY_STRING"])
    logging.warning(d)
    signature = d.get('signature',[''])[0]
    signature = escape(signature)
    timestamp = d.get('timestamp',[''])[0]
    timestamp = escape(timestamp)
    nonce = d.get('nonce',[''])[0]
    nonce = escape(nonce)
    echostr = d.get('echostr',[''])[0]
    echostr = escape(echostr)
    logging.warning(signature,timestamp,nonce,TOKEN)
    if check_signature(signature,timestamp,nonce,TOKEN):
        response_body = echostr
    else:
        response_body = "500 Bad request"
    response_header = [('Content-type', 'text/html'),('Content-Length',str(len(response_body)))]
    start_response(status,response_header)
    return resonse_body

application = WSGIApplication(app)
