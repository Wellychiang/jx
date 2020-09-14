from .page.login_page import LoginPage
from .page.deposit_page import DepositPage
from .page.home_page import HomePage
from selenium import webdriver
import pytest


url = 'http://www.sit.n51plus.ark88.local/Login'
sign = '?ReturnUrl=%2fAccount%2fManageCenter'
PageTitle = '聚星-登录'
username = 'wade01'
pwd = 'a111222'


@pytest.fixture()
def drive():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.close()


def test_login(drive):

    login = LoginPage(drive, url, PageTitle)

    login.open_browser()
    login.input_username(username)
    login.input_pwd(pwd)
    login.click_login()


# 記得homepage頁有更改
def test_deposit(drive, money=20):

    login = LoginPage(drive, url, PageTitle)
    deposit = DepositPage(drive, url, PageTitle)
    home = HomePage(drive, url, PageTitle)

    login.login(username, pwd)
    home.mouse_on_money()
    home.catch_money()
    home.click_to_recharge_page()
    home.switch_window()
    deposit.recharge(money)
    deposit.direct_pay_success()



