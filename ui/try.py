
from selenium import webdriver
from time import sleep

url = 'http://www.sit.n51plus.ark88.local/Login?ReturnUrl=%2fAccount%2fManageCenter'


def test_login():
    driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(5)
    driver.find_element_by_xpath("//*[@placeholder='帐号']").send_keys('wade01')
    driver.find_element_by_xpath("//*[@placeholder='密码']").send_keys('a111222')
    driver.find_element_by_xpath("//form[@id='formLogin']//input[@value='登  录']").click()
    sleep(5)
    a = driver.find_element_by_xpath("//*[@class='list']/span[@class='num'][1]").text
    for i in a:
        print('a: ' + i)

test_login()


