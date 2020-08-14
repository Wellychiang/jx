from base import Base
from selenium import webdriver
from time import sleep


class ui(Base):

    def test_login(self):
        driver = webdriver.Chrome()
        PageTitle = '聚星-登录'
        url = 'http://www.sit.n51plus.ark88.local/Login?ReturnUrl=%2fAccount%2fManageCenter'

        base = Base(driver, url, PageTitle)
        base.open()
        base.find_element("//*[@placeholder='帐号']").send_keys('wade01')
        base.find_element("//*[@placeholder='密码']").send_keys('a111222')
        base.find_element("//form[@id='formLogin']//input[@value='登  录']").click()

        sleep(3)


if __name__ == '__main__':
    ui().test_login()
