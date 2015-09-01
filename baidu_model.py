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
        self.session.open(self.baidu_url)
        self.session.open(self.baidu_login_url)
        code = Verification_Code()
        win = ''
        while 1:
            if  u'请输入验证码' in self.session.content or u'请您填写验证码' in self.session.content:
                print u'正在输入验证码'
                bsoup = BeautifulSoup(self.session.content)
                img_url = bsoup.find(id=self.img_selector)['src']
                code.save_img(img_url)
                result, num = code.parese_img()
                print result
                self.session.evaluate(
                    'document.getElementById("TANGRAM__PSP_3__verifyCode").value = "{res}";'.format(
                        res=result,
                    ))
                time.sleep(1)
                self.session.evaluate('document.getElementById("TANGRAM__PSP_3__submit").click();')
                if self.session.wait_for_text(u'登录成功') or self.session.wait_for_text(u'帐户设置'):
                    self.session.capture_to('ok.jpg')
                    self.use_hacker += num
                    time.sleep(2)
                    # 百度首页的 个人id   s_username_top
                    #                  等待加载这个试试
                    page,result = self.session.open(r'http://i.baidu.com',timeout=50)
                    if page.url == 'http://i.baidu.com/':
                         return u"""
                                  登录成功!
                                  使用验证码次数：{code_num}
                                  当前URL：{now_url}
                            """.format(code_num=self.use_hacker, now_url=page.url)

                    else:
                        print u'登录失败, 重新登录'
                        self.session.open(self.baidu_login_url)
                        continue
            else:
                print u'直接输入账号密码'
                self.session.show()
                self.check_parese()
                self.session.click(self.submit_selector)
                self.session.show()

    def check_parese(self):
        self.session.set_field_value(self.user_selector, self.uid)
        self.session.set_field_value(self.passwd_selector, self.passwd)



if __name__ == '__main__':
    baidu = BaiDu(uid='3321@sogou.com',
                  passwd='321321')

    print baidu.login()
