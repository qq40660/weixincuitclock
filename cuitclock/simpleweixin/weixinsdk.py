#-*- coding:utf-8 -*-
__author__ = 'Alexander.Li'
import logging

TEXT = u'text'
IMAGE = u'image'
LOCATION = u'location'
LINK = u'link'
EVENT = u"event"

def check_signature(token, params):
    '''
        验证微信加密签名
    '''
    import hashlib
    signature = params.get("signature")  #微信加密签名
    timestamp = params.get("timestamp")  #时间戳
    nonce = params.get("nonce")          #随机数
    echostr = params.get("echostr")      #随机字符串
    ##未进行参数字典排序？
    ##src = "".join([token, timestamp, nonce])
    src = "".join(sorted([token, timestamp, nonce]))
    m = hashlib.sha1()
    m.update(src)
    agro = m.hexdigest()
    if agro == signature:
        return echostr #原样返回echostr参数内容，接入生效
    output = "%s is not %s"%(agro,signature)
    logging.debug(output)
    return output

def __parseContent(xml):
    '''
        解析xml为字典
    '''
    from xml.dom.minidom import parseString
    dom = parseString(xml)
    root = dom.childNodes[0]
    return dict([(node.tagName, node.firstChild.nodeValue) for node in root.childNodes if node.nodeType==1])


def __generateContent(data):
    '''
        构造回复xml内容
    '''
    sequence = []
    if isinstance(data,dict):
        for key,value in data.iteritems():
            if isinstance(value,str) or isinstance(value,unicode):
                sequence.append("<%(tag)s><![CDATA[%(v)s]]></%(tag)s>"%dict(tag=key,v=value))
                continue
            if isinstance(value,list):
                sequence.append("<%(tag)s>%(v)s</%(tag)s>"%dict(tag=key,v=__generateContent(value)))
                continue
            if isinstance(value,dict):
                sequence.append("<%(tag)s>%(v)s</%(tag)s>"%dict(tag=key,v=__generateContent(value)))
                continue
            sequence.append("<%(tag)s>%(v)s</%(tag)s>"%dict(tag=key,v=value))
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                sequence.append("<item>%s</item>"%__generateContent(item))
                continue
            if isinstance(item, list):
                sequence.append("<item>%s</item>"%__generateContent(item))
                continue
            if isinstance(value,str) or isinstance(value,unicode):
                sequence.append("<item><![CDATA[%s]]></item>"%item)
                continue
            sequence.append("<item>%s></item>"%item)
    return "".join(sequence)

def __generateXml(data):
    '''
        生成完整xml
    '''
    return "".join(['<xml>',__generateContent(data),'</xml>'])


def response_text(content):
    '''
        文本消息
    '''
    return dict(Content=content)


def response_music(title,description,url,hd_url):
    '''
        音乐消息
    '''
    return dict(Music = dict(Title = title, Description = description, MusicUrl = url, HQMusicUrl = hd_url))


class Article(object):
    def __init__(self, title, description, picurl, url):
        self.title = title
        self.description = description
        self.picurl = picurl
        self.url = url

def response_html(articles):
    '''
        图文消息
    '''
    if articles and isinstance(articles[0],type(Article)):
        return dict(
            Articles = [
                dict(Title = article.title, Description = article.description, PicUrl = article.picurl, Url = article.url)
                for article in articles
            ]
        )
    raise TypeError, u"Must be the list of Article class"


def process_request(data, callback):
    '''
        处理来自post的请求
    '''
    params = __parseContent(data)
    logging.debug("get params %s"%params)
    reply = dict(
            ToUserName = params["FromUserName"],
            FromUserName = params["ToUserName"],
            CreateTime = params["CreateTime"],
            MsgType = params['MsgType'],
            FuncFlag = 0
    )
    reply.update(callback(params['MsgType'],params)) #动态添加消息内容
    return __generateXml(reply)
