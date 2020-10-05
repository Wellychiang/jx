from base import Base
from selenium import webdriver
import time
import pytest
import pytest_check as check
import os
import logging
import allure

init = Base('sit')

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


# AlipayPdd(10), WeiXinPdd(10), AlipayH5(10), WapBank(10), WeiXinScan(19), (USDT先別測, 需要Apollo的TradeNo)Usdt(10)
def for_failed(username='jackson', bank_type='WeiXinScan', amount='19'):

    response = init.login(username)
    failed_message = init.recharge(username, bank_type, amount, response['data']['key'])

    check.equal(False, failed_message['IsSuccess'], f'Real response: {failed_message}')
    check.is_in('目前没有渠道支援, 请选择其它充值方式', failed_message['ResponseMessage'], f'Real response: {failed_message}')
    check.equal('', failed_message['Url'], f'Real response: {failed_message}')
    check.equal(True, failed_message['DoVerify'], f'Real response: {failed_message}')


# 需注意Apollo一個帳號送出一定的充值單量就會卡住
# ()裡的值為最小限額
# Pdd的無法選擇錢, 但輸入參數的值還是會有影響(一鍵充值)
# 有確定送到Apoollo並確認訂單金額, 使用者
# AlipayPdd(10), WeiXinPdd(10), AlipayH5(10), WapBank(10), WeiXinScan(19), (USDT先別測, 需要Apollo的TradeNo)Usdt(10)
def common_recharge(setup_driver, username='jackson', bank_type='AlipayH5', amount='10'):
    response = init.login(username)
    # 充值
    recharge_response = init.recharge(username, bank_type, amount, response['data']['key'])
    # 充值 response 驗證
    check.equal(True, recharge_response['IsSuccess'])
    check.equal(True, recharge_response['DoVerify'])
    check.equal(float(amount + '.0'), recharge_response['VerifyMinAmount'])
    check.is_in(str(amount), recharge_response['ShowMin'])
    check.is_in('http://recharge.sit.n51plus.ark88.local/Pay.aspx?Amount=', recharge_response['Url'])
    # 到Apollo驗證有單且名字和錢一致
    time.sleep(2)
    setup_driver.find_element_by_xpath(merchant_order).click()
    time.sleep(2)
    setup_driver.find_element_by_xpath(Nike).click()
    setup_driver.find_element_by_xpath(order_reason_after_click_Nike).send_keys('qa')
    setup_driver.find_element_by_xpath(ok_after_write_order_reason).click()
    information = setup_driver.find_element_by_xpath("//*[@class='ui-widget-content slick-row even active' and @style='top:0px']")
    logging.debug(information.text)
    check.is_in(username, information.text)
    check.is_in(str(amount), information.text)


# 需注意Apollo一個帳號送出一定的充值單量就會卡住
# ()裡的值為最小限額
# 有確定送到Apoollo並確認訂單金額, 使用者
# 轉卡類case: bank(11), alipay_bank(70), wechat_bank(70)
def card_recharge(setup_driver, username='jackson', bank_type='wechat_bank', amount='80'):
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
    logging.debug(information.text)
    check.is_in(username, information.text)
    check.is_in(str(amount), information.text)


# ()裡的值為最小限額
# 轉卡類case: bank(11), alipay_bank(70), wechat_bank(70)
def card_for_failed(username='jackson', bank_type='alipay_bank', amount='69'):
    response = init.login(username)
    recharge_response = init.recharge(username, bank_type, amount, response['data']['key'])

    # 因三種轉卡類的response不同, 所以需要個別拉出來判斷
    if bank_type == 'bank':
        check.equal(False, recharge_response['success'])
        check.equal('目前没有渠道支援, 请选择其它充值方式(3)', recharge_response['message'])
    elif bank_type == 'alipay_bank' or bank_type == 'wechat_bank':
        check.equal(False, recharge_response['success'])
        check.is_in(f'交易金额: ¥70.00', recharge_response['message'])


@allure.feature('Positive')
def test_alipaypdd(setup_driver, bank_type='AlipayPdd', amount='10'):
    common_recharge(setup_driver, bank_type=bank_type, amount=amount)


@allure.feature('Positive')
def test_weixinpdd(setup_driver, bank_type='WeiXinPdd', amount='10'):
    common_recharge(setup_driver, bank_type=bank_type, amount=amount)


@allure.feature('Positive')
def test_alipayh5(setup_driver, bank_type='AlipayH5', amount='10'):
    common_recharge(setup_driver, bank_type=bank_type, amount=amount)


@allure.feature('Positive')
def test_wapbank(setup_driver, bank_type='WapBank', amount='10'):
    common_recharge(setup_driver, bank_type=bank_type, amount=amount)


@allure.feature('Positive')
def test_weixinscan(setup_driver, bank_type='WeiXinScan', amount='19'):
    common_recharge(setup_driver, bank_type=bank_type, amount=amount)


@allure.feature('Positive')
def test_bank(setup_driver, bank_type='bank', amount='11'):
    card_recharge(setup_driver, bank_type=bank_type, amount=amount)


@allure.feature('Positive')
def test_alipaybank(setup_driver, bank_type='alipay_bank', amount='70'):
    card_recharge(setup_driver, bank_type=bank_type, amount=amount)


@allure.feature('Positive')
def test_wechatbank(setup_driver, bank_type='wechat_bank', amount='70'):
    card_recharge(setup_driver, bank_type=bank_type, amount=amount)


@allure.feature('Minus')
def test_alipaypdd_failed(bank_type='AlipayPdd', amount='9'):
    for_failed(bank_type=bank_type, amount=amount)


@allure.feature('Minus')
def test_weixinpdd_failed(bank_type='WeiXinPdd', amount='9'):
    for_failed(bank_type=bank_type, amount=amount)


@allure.feature('Minus')
def test_alipayh5_failed(bank_type='AlipayH5', amount='9'):
    for_failed(bank_type=bank_type, amount=amount)


@allure.feature('Minus')
def test_wapbank_failed(bank_type='WapBank', amount='9'):
    for_failed(bank_type=bank_type, amount=amount)


@allure.feature('Minus')
def test_weixinscan_failed(bank_type='WeiXinScan', amount='18'):
    for_failed(bank_type=bank_type, amount=amount)


@allure.feature('Minus')
def test_bank_failed(bank_type='bank', amount='10'):
    card_for_failed(bank_type=bank_type, amount=amount)


@allure.feature('Minus')
def test_alipaybank_failed(bank_type='alipay_bank', amount='69'):
    card_for_failed(bank_type=bank_type, amount=amount)


@allure.feature('Minus')
def test_wechatbank_failed(bank_type='wechat_bank', amount='69'):
    card_for_failed(bank_type=bank_type, amount=amount)


if __name__ == '__main__':
    # del /q 能不提示直接刪除檔案夾(report)裡的東西
    os.system('del /q report')
    pytest.main(['-vs', '--alluredir', 'report'])
    os.system('allure generate report --clean')
    os.system('allure open')
