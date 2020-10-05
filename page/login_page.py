from common import base
from time import sleep


class LoginPage(base.Base):

    acc = "//*[@placeholder='帐号']"
    pwd = "//*[@placeholder='密码']"
    sign_in_button = "//form[@id='formLogin']//input[@value='登  录']"

    def open_browser(self):
        self.open()

    def input_username(self, username):
        self.find_element(self.acc).send_keys(username)

    def input_pwd(self, pwd):
        self.find_element(self.pwd).send_keys(pwd)

    def click_login(self):
        self.find_element(self.sign_in_button).click()

    def close(self):
        self.driver.close()

    def login(self, username, pwd):
        self.open_browser()
        self.input_username(username)
        self.input_pwd(pwd)
        self.click_login()
