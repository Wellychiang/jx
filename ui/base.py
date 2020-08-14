from element import Element
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time


class Base:

    acc = Element.login_page['account']
    pwd = Element.login_page['password']
    sign_in = Element.login_page['sign_in_button']

    def __init__(self, driver=None, url=None, page_title=None):
        self.driver = driver
        self.url = url
        self.page_title = page_title

    def find_element(self, args):
        try:
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_xpath(args)).is_displayed()
            return self.driver.find_element_by_xpath(args)

        except:
            return 'Can not find the' + str(args) + "'s element"

    def open(self):
        self.driver.get(self.url)
        self.driver.maximize_window()
        assert self.check_title(), "Page's title does'nt match driver's title, title: " + self.driver.title

    def check_title(self):
        return self.page_title in self.driver.title

    def _close(self):
        self.driver.close()

    def _login(self, username, pwd):
        self.open()
        self.find_element(self.acc).send_keys(username)
        self.find_element(self.pwd).send_keys(pwd)
        self.find_element(self.sign_in).click()

    def _switch_window(self):
        # from selenium import webdriver
        # drive = webdriver.Chrome()
        # drive.find_element()
        # drive.window_handles
        # drive.current_window_handle
        # drive.switch_to_window()
        windows = self.driver.window_handles
        print(windows)
        self.driver.switch_to_window(windows[1])

    def _sleep(self, times: int):
        time.sleep(times)

    def _loading(self):
        self.find_element("//div[contains(@id, 'maskOfPro')]")
