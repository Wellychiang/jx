from login_page import LoginPage
from deposit_page import DepositPage
from home_page import HomePage
from selenium import webdriver


url = 'http://www.sit.n51plus.ark88.local/'
sign = 'Login?ReturnUrl=%2fAccount%2fManageCenter'
PageTitle = '聚星-登录'
username = 'wade01'
pwd = 'a111222'
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# driver.get(url+sign)
# driver.find_element_by_xpath("//*[@placeholder='帐号']").send_keys('wade01')
# driver.find_element_by_xpath("//*[@placeholder='密码']").send_keys('a111222')
# driver.find_element_by_xpath("//form[@id='formLogin']//input[@value='登  录']").click()
# sleep(5)
# driver.find_element_by_xpath("//*[@class='btn_dropdown']").click()
# a = driver.find_element_by_xpath("//*[@id='divHomeBalance']//div[1]/div[2]/span[2]").text
#
#
# print('a: ' + a)
# driver.close()


def login():

    login = LoginPage(driver, url + sign, PageTitle)

    login.open_browser()
    login.input_username(username)
    login.input_pwd(pwd)
    login.click_login()
    login.close()


# 記得homepage頁有更改
def test_deposit(money=20):
    login = LoginPage(driver, url + sign, PageTitle)
    deposit = DepositPage(driver, url + sign, PageTitle)
    home = HomePage(driver, url + sign, PageTitle)

    login.login(username, pwd)
    home.mouse_on_money()
    home.catch_money()
    home.click_to_recharge_page()
    home.switch_window()
    deposit.recharge(money)
    print(2)
    deposit.direct_pay_success()



