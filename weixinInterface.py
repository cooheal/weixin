# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib,urllib2
import json
from lxml import etree
import re
import requests
class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        #获取输入参数
        data = web.input()
        signature = data.signature#加密签名
        timestamp = data.timestamp#时间戳
        nonce = data.nonce#s随机数
        echostr = data.echostr#随机字符串
        #自己的token
        token = "fanbaohong107"
        #字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,list)
        hashcode = sha1.hexdigest()
        #sha1加密算法        
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            return echostr
        
    def POST(self):
        str_xml = web.data() #获得post来的数据
        xml = etree.fromstring(str_xml)#进行XML解析
        mstype = xml.find("MsgType").text#消息类型
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        if mstype == 'text':
            content = xml.find("Content").text#获得用户所输入的内容
            info = content.encode('UTF-8') 
            key = '03745c73377a4ef89b6c8ade35e22cae' ###图灵机器人的key 
            userid=fromUser
            payload={'key':key,'info':info,'userid':userid}
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            s=requests.sessions.Session()
            s.headers.update(headers)
            r = s.post('http://www.tuling123.com/openapi/api', data=payload)
            code=r.json()['code']
            reply_content=r.json()['text']
                #reply_content+=str(code)
            if code==200000:
                url=r.json()['url']
                reply_content=reply_content+'\n'+url
            elif code==302000:
                slist=r.json()['list']
                for each in slist[:10]:
                    article=each['article']
                    #source=each['source']
                    detailurl=each['detailurl']
                    reply_content=reply_content+'\n'+article+'\n'+detailurl
            elif code==308000:
                slist=r.json()['list']
                name=slist[0]['name']
                #icon=each['icon']
                info=slist[0]['info']
                detailurl=slist[0]['detailurl']
                reply_content=reply_content+u'\n菜名：'+name+u'\n用料：'+info+'\n'+detailurl
            return self.render.reply_text(fromUser,toUser,int(time.time()),reply_content)
        
        elif mstype=='event':
            content=xml.find('Event').text
            if content=='subscribe':
                relpy_content=u'欢迎关注纯视公众微信号！纯视旨在依托微信公众号平台提供纷繁复杂信息的最简便获取入口，输入“help”获取功能列表。'
                return self.render.reply_text(fromUser,toUser,int(time.time()),relpy_content)
            if content=='unsubscrible':
                relpy_content=u'宝宝刚出生不久，目前能为你做的事情还很少，你的离开使我很难过，但本宝宝会努力使您再回到我身边的，一起加油！'
                return self.render.reply_text(fromUser,toUser,int(time.time()),relpy_content)

