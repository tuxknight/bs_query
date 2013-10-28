#!/bin/python
#-*-coding:UTF-8-*-
#Author: 褚夫元 <chufuyuan@foxmail.com>
__VERSION__ = 0.3

#import http.client
import httplib
import json
import socket
import random

class Bs:
    net = '0'
    BSID = '0'
    #HOST = 'apis.juhe.cn'
    HOST = 'v.juhe.cn'
    __KEY__ = {'g':('f17e16be2871e09e7669b0c0abe03342','f9ab0d5901ecc5265b79a0071a6a32e2'),
           'c':('d4ba46dd5a85d76a642350fcd62a951f','70fba5e2cdf581525498b412f74d3aba')
           }
    __HEX__ = '16'
    Fatal_code = ('444','112')
    G_rcode = {    '101':'appKey错误','203':'查询不到记录','200':'成功的返回',
                   '112':'当前请求可能已超过限制,请稍后再试或与客服联系!'
    }
    C_rcode = {    '101':'appKey错误','201':'SID错误','202':'Nid错误',
              '203':'Cellid错误','204':'系统出错','205':'查询不到记录',
              '200':'成功的返回','112':'当前请求可能已超过限制,请稍后再试或与客服联系!'
    }
    r_code = {}
    aid = '460310000'
    lng = ''
    lat = ''
    o_lat = ''
    o_lng = ''
    address = ''
    precision = ''
    reason = ''
    resultcode = ''
    def __init__(self,BSID):
        self.BSID = BSID
        if BSID[0:1] == '4':
            self.net = 'g'
            self.r_code = self.G_rcode
        
        elif BSID[0:1] == '3':
            self.net = 'c'
            self.r_code = self.C_rcode
	else:
	    self.net = 'g'
	    self.r_code = self.G_rcode
        


    def getUrl(self):
	length = len(self.__KEY__[self.net])
	rand = random.randrange(0,length)
        KEY = self.__KEY__[self.net][rand]
        if self.net == 'c':
            sid = self.BSID[0:4]
            nid = self.BSID[4:8]
            cellid = self.BSID[8:12]
            GET = '/cdma/?sid='+sid+'&cellid='+cellid+'&nid='+nid+'&hex='+self.__HEX__+'&key='+KEY
        elif self.net == 'g':
            cell = self.BSID[9:13]
            lac = self.BSID[5:9]
            GET = '/cell/get?cell='+cell+'&lac='+lac+'&hex='+self.__HEX__+'&key='+KEY
        return GET

    def fetchJson(self):
        try:
            #conn = http.client.HTTPConnection(self.HOST)
            conn = httplib.HTTPConnection(self.HOST)            
            GET = self.getUrl()
            conn.request('GET',GET)
            res = conn.getresponse()
            
            data = res.read().decode('utf-8')
            conn.close()
            
        except socket.gaierror:
            raise socket.gaierror
        except socket.timeout:
            raise socket.timeout

        return data
            

    def doSearch(self):
        try:
            jsonData = self.fetchJson()
        except socket.gaierror:
            raise socket.gaierror
        except socket.timeout:
            raise socket.timeout
        info = json.loads(jsonData)
        self.resultcode = info['resultcode']
        if self.resultcode == '200':
            if self.net == 'g':
                self.reason = info['reason']
                result = info['result']['data']
                #result的长度
                result = result[0]

                self.lng = str(result['LNG'])
                self.lat = str(result['LAT'])
                self.o_lng = str(result['O_LNG'])
                self.o_lat = str(result['O_LAT'])
                self.address =str(result['ADDRESS'])
                self.precision = str(result['PRECISION'])+'米'
            elif self.net == 'c':
                self.reason = info['reason']
                result = info['result']
                self.lng = str(result['lon'])
                self.lat = str(result['lat'])
                self.address = str(result['address'])
                self.precision = str(result['raggio'])+'米'
        else:
            self.reason = info['reason']

    def resultSet(self):
        try:
            self.doSearch()
        except socket.gaierror:
            self.resultcode = '444'
            return 'Resolve host failed.'
        except socket.timeout:
            self.resultcode = '444'
            return 'Time out.'
        
        if self.resultcode == '200':
            details = (self.BSID,self.aid,self.lng,self.lat,self.address,self.precision)
            rSet = '\t'.join(details)
            return rSet
        else:
            try:
                details = (self.BSID,self.r_code[self.resultcode])
                rSet = ':'.join(details)
            except KeyError:
                details = (self.BSID,'Code('+self.resultcode+')',self.reason)
                rSet = ':'.join(details)
            finally:
                return rSet




if __name__ == '__main__':
    #BSID = '3610000E1103'
    #BSID = '3610000E0092'
    #BSID = '46000185DE122'
    #BSID = '46001A8042A01'
    import sys
    import time
    reload(sys)
    sys.setdefaultencoding('utf-8')
    list = ('3610000E1103','46000185DE122','3610000E0092','46001A8042A01')
    c = 0
    head = ('BSID','经度','纬度','基站描述','覆盖半径')
    for i in list:
        if c == 0:
            print '\t'.join(head).encode('gb2312')
        c = c+1

        bs1 = Bs(i)
        result = bs1.resultSet()
        print result.encode('gb2312')
        '''        try:
            bs1.doSearch()
        except socket.gaierror:
            print 'Resolve host failed.' 
            break
        except socket.timeout:
            print 'Time out.' 
            break
        if bs1.resultcode == '200':
            print "%s\t%s\t%s\t%s\t%s" %(bs1.BSID,bs1.lng,bs1.lat,bs1.address,bs1.precision) 
        else:
            try:
                print "%s:%s" %(bs1.BSID,bs1.r_code[bs1.resultcode]) 
            except KeyError:
                print "%s:%s" %(bs1.resultcode,bs1.reason) 
                break
        '''
