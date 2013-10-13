#-*- coding:utf-8 -*-
from bae.core.wsgi import WSGIApplication
from  wri_bsid_search import *
from cgi import parse_qs, escape
import markdown
reload(sys)
sys.setdefaultencoding('utf-8')
list = ('3610000E1103','46000185DE122','3610000E0092','46001A8042A01')
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
for i in list:
    if c == 0:
        #print '\t'.join(head).encode('gb2312')
        body='\t'.join(head).encode('utf-8')
    c = c+1
    bs1 = Bs(i)
    result = bs1.resultSet()
    body = body + '</br>' + result.encode('utf-8')

def md2html(mkdn):
    return markdown.markdown(mkdn)

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
#    response_body = html % (bsid,'2','3')
#    response_header = [headers,('Content-Length',str(len(response_body)))]
#    start_response(status,response_header)
#    return response_body
    d = parse_qs(environ['QUERY_STRING'])
    bsid = d.get('bsid',[''])[0]
    bsid = escape(bsid)
    response_body = response_md % (bsid,'2','3')
    response_header = [('Content-type', 'text/html'),('Content-Length',str(len(response_body)))]
    start_response(status,response_header)
    #return body
    return  md2html(response_body) 
application = WSGIApplication(app)
