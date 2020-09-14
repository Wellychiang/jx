from .base import Base
from selenium import webdriver
import time
import pytest_check as check

init = Base('sit')

 # AlipayH5
 # WapBank


def test_recharge_success(username='jackson'):

    response = init.login(username)
    init.recharge(username, 'AlipayH5', 100, response['data']['key'])

    # 這裡用headless會渲染不出金額導致用例失敗
    # options = Options()
    # options.add_argument('--headless')
    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome()

    driver.get('http://console.sit.apollo.ark88.local/Account/Login?ReturnUrl=%2f')
    driver.implicitly_wait(8)
    driver.find_element_by_xpath('//*[@name="Username"]').send_keys('jx')
    driver.find_element_by_xpath("//*[@name='Password']").send_keys('!QAZ2wsx')
    driver.find_element_by_xpath("//*[@type='submit']").click()

    driver.find_element_by_xpath("//*[span='Merchant']").click()
    driver.find_element_by_xpath("//a[@href='/MerchantManage/MerchantOrders']/span").click()

    a = driver.find_element_by_xpath("//*[@class='ui-widget-content slick-row even' and @style='top:0px']")
    check.is_in(username, a.text,)
    check.is_in('100', a.text)
    driver.close()


