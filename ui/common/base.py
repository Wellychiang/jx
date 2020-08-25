
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class Base:

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

    def _switch_window(self):

        windows = self.driver.window_handles
        self.driver.switch_to_window(windows[1])

    def sleep(self, times):
        sleep(times)
