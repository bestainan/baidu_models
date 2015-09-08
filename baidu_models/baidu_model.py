# -*- coding: utf-8 -*-
# author:Robot
# QQ:81999678
# E-mail:a.robot.n@gmail.com
# Tel:18777777105

import urllib, urllib2
import time
import sys
import re
from ghost import Ghost
from ghost import TimeoutError
from urllib import urlencode
from verification_code import Verification_Code
from bs4 import BeautifulSoup

ghost = Ghost()


class BaiDu():
    '''
    baidu models
    if you want send_post, you must login first
    '''

    def __init__(self, uid, passwd, proxy={}):

        self.use_hacker = 0
        self.return_url = ''
        self.return_img = ''
        self.session = ghost.start(display=True)
        self.code = Verification_Code()
        # try:
        #     self.session.set_proxy(type_= 'HTTPS',host='111.161.126.99',port=80)
        #     print u'代理开启成功'
        # except KeyError:
        #     pass

        self.uid = uid
        self.passwd = passwd

        self.baidu_url = r"https://www.baidu.com"
        self.baidu_login_url = r"https://passport.baidu.com"


        self.user_selector = "#TANGRAM__PSP_3__userName"
        self.passwd_selector = "#TANGRAM__PSP_3__password"
        self.submit_selector = "#TANGRAM__PSP_3__submit"
        self.img_selector = "TANGRAM__PSP_3__verifyCodeImg"
        self.input_wverifycode_selector = "TANGRAM__PSP_3__verifyCode"

    def login(self):
        self.session.open(self.baidu_login_url,timeout=60)
        coun = 0
        while 1:
            self.session.show()
            try:
                resquest =  self.session.evaluate("document.getElementById('TANGRAM__PSP_3__error').innerHTML;")[0]
                if coun >= 3:
                    page,b = self.session.open(self.baidu_login_url,timeout=60)
                    coun = 0

                elif u'登录成功' in self.session.content or 'ibx-uc' in self.session.content or u'快速通道' in self.session.content:
                    print u'登录成功'
                    self.session.capture_to('ok.jpg')
                    return self.use_hacker
                elif u'请输入验证码' == resquest or \
                                u'请您填写验证码' == resquest or \
                                u'您输入的验证码有误' == resquest:
                    print u'输入验证码'
                    result = self.pare_verifi()
                    self.session.evaluate(
                        'document.getElementById("TANGRAM__PSP_3__verifyCode").value = "{res}";'.format(
                            res=result,
                        ))
                    coun += 1
                    self.session.click("#TANGRAM__PSP_3__submit")
                elif u'请您填写手机/邮箱/用户名' == resquest:
                    print u'写账号'
                    self.session.set_field_value(self.user_selector, self.uid)

                elif u'请您填写密码' == resquest:
                    print u'写密码'
                    self.session.set_field_value(self.passwd_selector, self.passwd)

                elif u'登录超时' == resquest:
                    print u'点击提交'
                    self.session.click(self.submit_selector)

                elif u'登录中' in self.session.content:
                    print u'等待2秒'
                    time.sleep(2)

                elif resquest == '':
                    print u'点提交'
                    self.session.click(self.submit_selector)


                else:
                    page,b = self.session.open(self.baidu_login_url)
            except TimeoutError:
                continue

    def pare_verifi(self,img = None):
        if img:
            img_url = img
            self.code.save_img(img_url)
            result, num = self.code.parese_img()
            self.use_hacker += num
            return result
        else:
            bsoup = BeautifulSoup(self.session.content)
            img_url = bsoup.find(id=self.img_selector)['src']
            self.code.save_img(img_url)
            result, num = self.code.parese_img()
            self.use_hacker += num
            return result

    def post_msg(self,url,info):
        print u'初始化'
        img_url_selector = "document.querySelector('.j_captcha_img_wrapper img').src"
        input_img_selector = "document.querySelector('.tbui_captcha_input_wrap .j_captcha_input').value ='%s'"
        img_submit_bt_selector = ".ui_btn_m"
        submit_bt_selector = "div .j_floating > a"
        title_selector = "document.querySelector('input[name=\"title\"]').value = '%s'"
        content_selector = "document.querySelector('#ueditor_replace p').innerHTML= '%s'"
        for _key,_item in info.items():
            print u'转换类型'
            if not isinstance(_item, unicode):
                try:
                    info[_key] = unicode(_item,'utf-8')
                except TypeError:
                    continue
        title = info.get('title',None)
        content = info.get('content',None)
        stop = 1
        while stop:
            try:
                print u'开启网站'
                self.session.open(url)
            except:
                print u'判断是否可以继续'
                if self.session.evaluate("document.querySelector('#tb_nav')")[0]:
                    self.session.show()
                    print u'#缓慢滚动到最底部'
                    self.roll_window()
                else :
                    continue
                print u'写入 标题 内容'
                self.session.evaluate(title_selector % title)
                self.session.evaluate(content_selector % content)
                while stop:
                    try:
                        self.session.click(submit_bt_selector)
                        try:
                            self.session.wait_for_text(u'发表成功')
                            print u'#不需要验证码直接成功'
                            self.session.capture_to('ok.jpg')
                            stop = 0
                            break
                        except:
                            print u'#需要验证码'
                            self.session.wait_for_text(u"请输入验证码完成发贴")
                            print u'#输入验证码'
                            img_url = self.session.evaluate(img_url_selector)[0]
                            result = self.pare_verifi(img_url)
                            self.use_hacker += 1
                            self.session.evaluate(input_img_selector % result )
                            while 1:
                                print u'#循环点击按钮'
                                self.session.click(img_submit_bt_selector)
                                try:
                                    self.session.wait_for_text(u'发表成功')
                                    self.session.show()
                                    stop = 0
                                    print u'成功'
                                    break
                                except:
                                    print u'验证码失败重试'
                                    self.session.wait_for_text(u"请输入验证码完成发贴")
                                    continue

                            break
                    except:
                        continue
        print u'使用验证码共计:' , self.use_hacker



    def roll_window(self):
        #缓慢滚动到最底部
        self.window_height_str = int(self.session.evaluate('document.body.scrollHeight')[0])
        temp_height_str = 0
        while temp_height_str < self.window_height_str:
            self.session.evaluate('window.scrollTo(0,%s);' % temp_height_str)
            while 1:
                if self.session.evaluate('document.readyState')[0] != "loading":
                    print self.session.evaluate('document.readyState')[0]
                    break

                else:
                    time.sleep(0.3)
                    self.session.show()
                    print u'等待加载'
            self.session.show()
            temp_height_str +=  500
        self.session.evaluate('window.scrollTo(0,document.body.scrollHeight);')


    def __del__(self):
        del self.session


#todo:再看看能不能解决 url的问题
if __name__ == '__main__':

    baidu = BaiDu(uid='aqvjrv87148@163.com',
                  passwd='Q2jQHk')

    print u'登录完成 验证码使用次数:{num}'.format(num = baidu.login())
    # baidu.baidu_reply()
    # baidu.baidu_post_msg()
    info = {
        'title':'这里是标题',
        'content':u'我是新来的~~~'
    }
    '''
    http://tieba.baidu.com/f?kw=%E8%84%89%E5%8A%A8&ie=utf-8

    http://tieba.baidu.com/f?kw=%C9%D9%C4%EA%CB%C4%B4%F3%C3%FB%B2%B6
    '''
    while 1:
        baidu.post_msg(url = 'http://tieba.baidu.com/f?kw=%C9%D9%C4%EA%CB%C4%B4%F3%C3%FB%B2%B6',info=info)