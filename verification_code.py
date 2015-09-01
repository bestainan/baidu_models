#coding:utf-8
import re
import urllib
import urllib2
import os
import time
VERIFICATION_IMG_PATH = "verification_imgs/"
HACKER_URL = "http://192.168.100.108/vcode/test.php"
class Verification_Code:
    '''
    破解验证码
    return : u'验证码'
    '''
    def save_img(self,img_url):
        '''
        保存验证码图片
        '''
        try:
            os.mkdir('verification_imgs/')
        except:
            pass
        self.img_url = img_url
        conn = urllib.urlopen(img_url)
        with open(VERIFICATION_IMG_PATH + 'img.png','wb') as file:
            file.write(conn.read())


    def parese_img(self):
        '''
        解析 图片
        '''
        with open(VERIFICATION_IMG_PATH + 'img.png','rb') as file:
            img = file.read()

            url = "http://192.168.100.108/vcode/test.php"
            dat = {
            "code":img,
            "type":62,
            }
            data = urllib.urlencode(dat)
            req = urllib2.Request(url,data)
            resp = urllib2.urlopen(req,timeout=25)
            code = resp.read()
            return  code.decode('utf-8'),1


if __name__ == '__main__':
    pass