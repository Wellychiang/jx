from .base import Base
from selenium import webdriver
import time
import pytest
import pytest_check as check
init = Base('sit')


 # AlipayH5
 # WapBank
url = 'http://console.sit.apollo.ark88.local/Account/Login?ReturnUrl=%2f'


user_input = '//*[@name="Username"]'
pwd_input = "//*[@name='Password']"
submit = "//*[@type='submit']"
merchant = "//*[span='Merchant']"
merchant_order = "//a[@href='/MerchantManage/MerchantOrders']/span"
first_line_information = "//*[@class='ui-widget-content slick-row even' and @style='top:0px']"
Nike = "//a[@class='inline-action Succeeded']"
order_reason_after_click_Nike = "//input[@id='Memo']"
ok_after_write_order_reason = "//button[contains(text(),'OK')]"


@pytest.fixture()
def setup_driver(apollo_account='jx', apollo_pwd='!QAZ2wsx'):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(8)
    driver.find_element_by_xpath(user_input).send_keys(apollo_account)
    driver.find_element_by_xpath(pwd_input).send_keys(apollo_pwd)
    driver.find_element_by_xpath(submit).click()

    driver.find_element_by_xpath(merchant).click()
    yield driver

    driver.close()


# AlipayPdd(10),WeiXinPdd(10), AlipayH5(100), WapBank(500), WeiXinScan(100), Usdt(10)
def for_failed(username='jackson', bank_type='AlipayH5', amount='100'):

    response = init.login(username)
    failed_message = init.recharge(username, bank_type, amount, response['data']['key'])

    check.equal(False, failed_message['IsSuccess'], f'Real response: {failed_message}')
    check.is_in('目前没有渠道支援, 请选择其它充值方式', failed_message['ResponseMessage'], f'Real response: {failed_message}')
    check.equal('', failed_message['Url'], f'Real response: {failed_message}')
    check.equal(True, failed_message['DoVerify'], f'Real response: {failed_message}')


# 需注意Apollo一個帳號送出一定的充值單量就會卡住
# ()裡的值為最小限額
# Pdd的無法選擇錢(一鍵充值)
# AlipayPdd(10),WeiXinPdd(10), AlipayH5(100), WapBank(500), WeiXinScan(100), Usdt(10)
def common(setup_driver, username='jackson', bank_type='AlipayH5', amount='10'):
    response = init.login(username)
    # 充值
    recharge_response = init.recharge(username, bank_type, amount, response['data']['key'])
    # 充值 response 驗證
    check.equal(True, recharge_response['IsSuccess'])
    check.equal(True, recharge_response['DoVerify'])
    check.equal(float(amount + '.0'), recharge_response['VerifyMinAmount'])
    check.is_in(str(amount), recharge_response['ShowMin'])
    check.is_in('http://recharge.sit.n51plus.ark88.local/Pay.aspx?Amount=', recharge_response['Url'])
    # 到Apollo驗證有單且名字和錢一致(業務邏輯)
    time.sleep(2)
    setup_driver.find_element_by_xpath(merchant_order).click()
    time.sleep(2)
    setup_driver.find_element_by_xpath(Nike).click()
    setup_driver.find_element_by_xpath(order_reason_after_click_Nike).send_keys('qa')
    setup_driver.find_element_by_xpath(ok_after_write_order_reason).click()
    information = setup_driver.find_element_by_xpath("//*[@class='ui-widget-content slick-row even active' and @style='top:0px']")
    print(information.text)
    check.is_in(username, information.text)
    check.is_in(str(amount), information.text)


# 需注意Apollo一個帳號送出一定的充值單量就會卡住
# ()裡的值為最小限額
# 轉卡類case: bank(70), alipay_bank(70), wechat_bank(70)
def bank(setup_driver, username='jackson', bank_type='wechat_bank', amount='80'):
    response = init.login(username)
    recharge_response = init.recharge(username, bank_type, amount, response['data']['key'])

    # 因三種轉卡類的response不同, 所以需要個別拉出來判斷
    if bank_type == 'bank':
        check.equal(True, recharge_response['success'])
        check.equal(2, recharge_response['data']['payType'])
        check.equal(float(amount + '.0'), recharge_response['data']['amount'])
    elif bank_type == 'alipay_bank':
        check.equal(True, recharge_response['success'])
        check.is_in(f'{amount}', recharge_response['data']['AttachWord'])
        check.is_in(f'{amount}', recharge_response['data']['Amount'])
        check.equal(2, recharge_response['data']['MoneyInType'])
    elif bank_type == 'wechat_bank':
        check.equal(True, recharge_response['success'])
        check.is_in(f'{amount}', recharge_response['message'])
        check.equal(True, recharge_response['result']['IsDeal'])
        check.equal(10, recharge_response['result']['MoneyInType'])
        check.equal(0, recharge_response['result']['Sort'])

    # Apollo的Api懶得抓, 直接用selenium跑且寫死部分參數
    time.sleep(2)
    setup_driver.find_element_by_xpath(merchant_order).click()
    time.sleep(2)
    setup_driver.find_element_by_xpath(Nike).click()
    setup_driver.find_element_by_xpath(order_reason_after_click_Nike).send_keys('qa')
    setup_driver.find_element_by_xpath(ok_after_write_order_reason).click()
    information = setup_driver.find_element_by_xpath("//*[@class='ui-widget-content slick-row even active' and @style='top:0px']")
    print(information.text)
    check.is_in(username, information.text)
    check.is_in(str(amount), information.text)


def test_reacharge_positive(setup_driver):
    bank(setup_driver, amount='70')


def test_recharge_minus():

    for_failed(amount='9')


