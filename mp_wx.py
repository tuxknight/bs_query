#-*- coding:utf-8 -*-
from bae.core.wsgi import WSGIApplication
from  wri_bsid_search import *
from cgi import parse_qs, escape
import sys
import hashlib
#import markdown
reload(sys)
sys.setdefaultencoding('utf-8')
TOKEN = "chufuyuan0420"
def check_signature(sig,stamp,nonc,tk)
    par = [tk,stamp,nonc]
    parstr = "".join(sorted(par))
    tmpstr = hashlib.sha1(parstr).hexdigest()
    if tmpstr == sig:
	return true
    else:
	return false

def app(environ, start_response)
    status = "200 OK"
    #解析 HTTP GET 的参数
    d = parse_qs(environ["QUERY_STRING"])
    signature = d.get('signature',[''])[0]
    signature = escape(signature)
    timestamp = d.get('timestamp',[''])[0]
    timestamp = escape(timestamp)
    nonce = d.get('nonce',[''])[0]
    nonce = escape(nonce)
    echostr = d.get('echostr',[''])[0]
    echostr = escape(echostr)

    if check_signature(signature,timestamp,noce,TOKEN):
	response_body = echostr

application = WSGIApplication(app)
