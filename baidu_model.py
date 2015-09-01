# coding:utf-8
import urllib, urllib2
import time
from ghost import Ghost
from ghost import TimeoutError
from verification_code import Verification_Code
from bs4 import BeautifulSoup

ghost = Ghost()


class BaiDu():
    '''
    百度的基本操作
    '''

    def __init__(self, uid, passwd, proxy={}):
        self.use_hacker = 0
        self.return_url = ''
        self.return_img = ''
        self.session = ghost.start()
        self.code = Verification_Code()
        try:
            self.session.delete_cookies()
            self.session.set_proxy(host=proxy['localhost'],
                                   port=proxy['port'],
                                   user=proxy['user'],
                                   password=proxy['password'])
        except KeyError:
            pass
        self.baidu_url = r"https://www.baidu.com"
        self.baidu_login_url = r"https://passport.baidu.com"
        self.uid = uid
        self.passwd = passwd
        self.user_selector = "#TANGRAM__PSP_3__userName"
        self.passwd_selector = "#TANGRAM__PSP_3__password"
        self.submit_selector = "#TANGRAM__PSP_3__submit"
        self.img_selector = "TANGRAM__PSP_3__verifyCodeImg"
        self.input_wverifycode_selector = "TANGRAM__PSP_3__verifyCode"

    def login(self):
        self.session.open(self.baidu_login_url)

        while 1:
            self.session.show()
            resquest =  self.session.evaluate("document.getElementById('TANGRAM__PSP_3__error').innerHTML;")[0]

            if u'登录成功' in self.session.content:
                self.session.show()
                return self.use_hacker
                self.session.show()
            elif u'请输入验证码' == resquest or \
                            u'请您填写验证码' == resquest or \
                            u'您输入的验证码有误' == resquest:

                result = self.pare_verifi()
                self.session.evaluate(
                    'document.getElementById("TANGRAM__PSP_3__verifyCode").value = "{res}";'.format(
                        res=result,
                    ))

                self.session.click("#TANGRAM__PSP_3__submit")
                self.session.show()
            elif u'请您填写手机/邮箱/用户名' == resquest:
                self.session.set_field_value(self.user_selector, self.uid)
                self.session.show()

            elif u'请您填写密码' == resquest:
                self.session.set_field_value(self.passwd_selector, self.passwd)
                self.session.show()

            elif u'登录超时' == resquest:
                self.session.click(self.submit_selector)
                self.session.show()

            elif u'登录中' in self.session.content:
                time.sleep(1)
                self.session.show()
            elif resquest == '':
                self.session.click(self.submit_selector)
                self.session.show()

    def pare_verifi(self):
        bsoup = BeautifulSoup(self.session.content)
        img_url = bsoup.find(id=self.img_selector)['src']
        self.code.save_img(img_url)
        result, num = self.code.parese_img()
        self.use_hacker += num
        return result

    def __del__(self):
        del self


if __name__ == '__main__':
    baidu = BaiDu(uid='pwubais628@sogou.com',
                  passwd='vtbianj317')

    print u'验证码使用次数:{num}'.format(num = baidu.login())
