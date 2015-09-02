# coding:utf-8
# author:Robot
# QQ:81999678
# E-mail:a.robot.n@gmail.com
# Tel:18777777105

import urllib, urllib2
import time
import re
from ghost import Ghost
from ghost import Session
from ghost import TimeoutError
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
        self.session = ghost.start()
        self.code = Verification_Code()
        try:
            # self.session.delete_cookies()
            self.session.set_proxy(host=proxy['localhost'],
                                   port=proxy['port'],
                                   user=proxy['user'],
                                   password=proxy['password'])
        except KeyError:
            pass

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
                    self.session.open(self.baidu_login_url,timeout=60)
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
                    self.session.open(self.baidu_login_url)
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

    def baidu_reply(self):
        '''
        url,info
        return OK_img
        '''
        print u'开始发帖'
        while 1:
            page,b = self.session.open(r"http://tieba.baidu.com/p/4014668676",timeout=120)
            assert page.http_status == 200 and u'<em>发 表</em>' in self.session.content
            self.session.wait_for_selector('#ueditor_replace')
            self.session.evaluate('window.scrollTo(0,document.body.scrollHeight);')
            time.sleep(2)
            self.session.evaluate('window.scrollTo(0,document.body.scrollHeight);')

            if self.session.wait_for_selector('#ueditor_replace'):
                self.session.show()
                print u'写内容'
                self.session.evaluate("document.getElementById('ueditor_replace').innerHTML = '12fdlgslkjflwejrr;lwejr3123123'")
                time.sleep(1)
                print u'等待按钮'
                self.session.wait_for_selector(".j_submit")
                time.sleep(3)

                # self.session.evaluate('document.getElementsByClassName("j_submit").id = "mysubmit";document.getElementById("mysubmit").click();')
                print self.session.evaluate('document.getElementsByClassName("j_submit").click()')
                self.session.wait_for_alert(timeout=120)
                self.session.capture_to('asd.jpg')

                time.sleep(3)
                self.session.show()




                print '2'
                # html = self.session.content
                # img_url = re.findall(r'<span class="tbui_captcha_img_wrap j_captcha_img_wrapper"><img src="(.*)"></span><span class="tbui_captcha_buttons">',html)
                # img_url = 'http://tieba.baidu.com' + img_url[0]
                # result = self.pare_verifi(img_url)
                # time.sleep(1)
                # a,b = self.session.evaluate("document.getElementsByClassName('j_captcha_input')")
                # print a
                # print ################
                # print b
                #
                # time.sleep(2)
                # self.session.wait_callback
                # self.session.capture_to('ok.jpg')
                # self.session.show()
                # raw_input('wait...')
                # self.session.click('.ui_btn ui_btn_m j_ok',expect_loading = True)
                # self.session.show()
                # raw_input('wait...')
                # self.session.evaluate(
                # 'document.getElementById("TANGRAM__PSP_3__verifyCode").value = "{res}";'.format(
                #     res=result,
                # ))
                # self.session.click("#TANGRAM__PSP_3__submit")
                # print img_url
                # except TimeoutError,e:
                #     print e
                #
                #     continue

                print u'拍照留念'
                self.session.capture_to('ok.jpg')
                break

    def baidu_post_msg(self,url):
        '''
        return post_url & the post_img
        '''
        self.session.open(r'http://tieba.baidu.com/f?kw=%CC%A9%B5%CF%D0%DC')
        pass



    def __del__(self):
        del self.session




if __name__ == '__main__':
    baidu = BaiDu(uid='pwubais628@sogou.com',
                  passwd='vtbianj317')

    print u'验证码使用次数:{num}'.format(num = baidu.login())
    baidu.baidu_reply()