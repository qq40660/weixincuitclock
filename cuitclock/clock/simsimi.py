#-*-coding:utf-8-*-
import requests
import cookielib
import os

class SimSimi:

    def __init__(self):
        r = requests.get('http://www.simsimi.com/talk.htm')
        self.cookies = r.cookies

        self.headers = {
            'Referer': 'http://www.simsimi.com/talk.htm'
        }
        self.url = 'http://www.simsimi.com/func/req?lc=ch&msg=%s'
        os.environ['disable_fetchurl'] = "1"
        
    def chat(self, message=''):
        if message.strip():
            r = requests.get(self.url % message.strip(), headers=self.headers, cookies=self.cookies)
            print r
            self.cookies = r.cookies
            try:
                return r.json()['response']
            except:
                return u'呵呵'
        else:
            return u'叫我干嘛'

if __name__ == '__main__':
    simi = SimSimi()
    print simi.chat('最后一个问题')


