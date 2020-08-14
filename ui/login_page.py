from base import Base
from element import Element
from time import sleep


class Login(Base):

    acc = Element.login_page['account']
    pwd = Element.login_page['password']
    sign_in = Element.login_page['sign_in_button']

    def open_browser(self):
        self.open()

    def input_username(self, username):
        self.find_element(self.acc).send_keys(username)

    def input_pwd(self, pwd):
        self.find_element(self.pwd).send_keys(pwd)

    def click_login(self):
        self.find_element(self.sign_in).click()
