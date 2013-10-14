#-*- coding:utf-8 -*-
from bae.core.wsgi import WSGIApplication
from  wri_bsid_search import *
from cgi import parse_qs, escape
import markdown
reload(sys)
sys.setdefaultencoding('utf-8')
#list = ('3610000E1103','46000185DE122','3610000E0092','46001A8042A01')
c = 0
head = ('BSID','经度','纬度','基站描述','覆盖半径')
body = ''
response_md = '''
<table>
<thead>
<tr> 
  <td>head1</td>
  <td>head2</td>
  <td>head3</td>
</tr>
</thead>
<tbody>
<tr>
  <td>%s</td>
  <td>%s</td>
  <td>%s</td>
</tbody>
</table>
'''
def md2html(mkdn):
    return markdown.markdown(mkdn)
def valid_bsid(bsid):
    c_LEN = 12
    g_LEN = 13
    length = len(bsid)
    if length < c_LEN or length > g_LEN:#非法长度
        return False
    elif length == c_LEN and bsid[0:1] != '3':#C网3开头，G网4开头
        return False
    elif length == g_LEN and bsid[0:1] != '4':
        return False
    else:
        return True
def app(environ, start_response):
    status = '200 OK'
    #headers = [('Content-type', 'text/html')]
    #start_response(status, headers)
    #body=["Welcome to Baidu Cloud!\n"]
    #return body
# HTTP POST
#    try:
#	request_body_size = int(environ.get('CONTENT_LENGTH',0))
#    except(ValueError):
#	request_body_size = 0
#    request_body = environ['wsgi.input'].read(request_body_size)
#    d = parse_qs(request_body)
#    bsid = d.get('bsid',[''])[0]
#    bsid = escape(bsid)
#    response_body = response_md % (bsid,'2','3')
#    response_header = [('Content-type', 'text/html'),('Content-Length',str(len(response_body)))]
#    start_response(status,response_header)
#    return response_body
    d = parse_qs(environ['QUERY_STRING'])
    bsid = d.get('bsid',[''])[0]
    bsid = escape(bsid)
    if not valid_bsid(bsid):
	response_body = "<tr><td>"+bsid+"</td><td>invalid id!!</td></tr>"
        response_header = [('Content-type', 'text/html'),('Content-Length',str(len(response_body)))]
        start_response(status,response_header)
        return response_body
    bs1 = Bs(bsid)
    try:
        bs1.doSearch()
    except socket.gaierror:
	response_body = "<tr><td>"+bsid+"</td><td>Resolve host failed.</td></tr>"
    except socket.timeout:
	response_body = "<tr><td>"+bsid+"</td><td>Time out.</td></tr>"
    if bs1.resultcode == '200':
        response_body = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %(bs1.BSID,bs1.lng,bs1.lat,bs1.address,bs1.precision) 
    else:
        try:
            response_body = "<tr><td>%s</td><td>%s</td></tr>" %(bs1.BSID,bs1.r_code[bs1.resultcode]) 
        except KeyError:
            response_body = "<tr><td>%s</td><td>%s</td><td>%s</td></tr>" %(bs1.BSID,bs1.resultcode,bs1.reason) 

    response_header = [('Content-type', 'text/html'),('Content-Length',str(len(response_body)))]
    start_response(status,response_header)
    return response_body
    #return  md2html(response_body) 
application = WSGIApplication(app)
