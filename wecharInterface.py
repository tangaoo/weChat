# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os, sys
import logging
import urllib2, urllib
import json
from lxml import etree

logging.basicConfig(filename='logger.log', level=logging.INFO)

def send_post(url, data):
	try:
		content_type = 'application/json'
		headers = {'Content-Type': content_type}
		req = urllib2.Request(url, data, headers)
		response = urllib2.urlopen(req)
		the_page = response.read()
	except:
		the_page = None
	return the_page

def send_get(url):
	try:
		req = urllib2.Request(url)
		f = urllib2.urlopen(req)
		html = f.read()
		return html
	except:
		return None

class WecharInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        # return "hi, boy!"
        data = web.input() #get input parameters
        logging.debug(data)
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = "ngsirnet" #set by yourself
        list = [token, timestamp, nonce]
        list.sort() #dictionary sorted
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest() #sha1 encryption

        if hashcode == signature:
            return echostr

    def POST(self):
        message_xml = web.data() #get post data frow wechar
        # logging.debug(message_xml)
        xml = etree.fromstring(message_xml) #analysis xml
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        if msgType == 'text':
            content = xml.find("Content").text
            if "18612345678" in content:
                expressNum = str(9640077808523)
            # if content[0:2] == u"快递":
                # expressNum = str(content[2:])

                url = 'http://www.kuaidi100.com/autonumber/autoComNum?text=%s' % (expressNum)

            	data = '{}'
            	page =  send_post(url, data)
            	if page == None:
            		print '请求失败'
            		sys.exit()
            	page = json.loads(page)
            	type =  page['auto'][0]['comCode']
            	id = page['num']
                # return (type, id)
                url = 'http://www.kuaidi100.com/query?type=%s&postid=%s' % (type, id)
            	ret = send_get(url)
                if ret:
                    ret = json.loads(ret)
                    data = ret['data']
                    string = u''
                    for info in data:
                        string = string + info['time'] + info['context'] + '\n'
                return self.render.replytext(fromUser,toUser,int(time.time()), string)
            else:
                return self.render.replytext(fromUser, toUser, int(time.time()), u'公众号在处于开发阶段，功能不完善，请见谅……')
        elif msgType == 'image':
			mediaId = xml.find("MediaId").text
			return self.render.replyimage(fromUser,toUser,int(time.time()), mediaId)
        else:
            return "success"
