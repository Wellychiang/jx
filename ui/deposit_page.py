from base import Base
from element import Element


class Deposit(Base):

    home = Element.home_page
    deposit = Element.deposit_page

    _mouse_on_money = home['mouse_on_money']
    _balance = home['balance']
    _deposit = home['deposit']

    _input_amount = deposit['input_money']
    _quick_recharge = deposit['quick_recharge']
    recharge_not_visible = deposit['recharge_not_visible']

    def login(self, username, pwd):
        self._login(username, pwd)

    def mouse_on_money(self):
        try:
            self.find_element(self._mouse_on_money).click()
        except:
            self._sleep(2)
            self.find_element(self._mouse_on_money).click()

    def catch_money(self):
        if self.find_element(self._balance).text.strip('¥') == '':
            self._sleep(2)
            print(self.find_element(self._balance).text)
        else:
            print(self.find_element(self._balance).text)

    def click_to_recharge_page(self):
        self.find_element(self._deposit).click()

    def switch_window(self):
        self._switch_window()

    def input_amount(self, coco):
        self.find_element(self._input_amount).send_keys(coco)

    def quick_recharge(self):
        self.find_element(self._quick_recharge).click()

    def recharge(self, coco=None):
        if self.recharge_not_visible:
            self.quick_recharge()

        else:
            self.input_amount(coco)

    def direct_pay_success(self):
        if '请输入银行卡姓名及金额以完成支付' in self.find_element("//div[@class = 'payment_system_content']/h1").text:
            pass
        else:
            self.driver.save_screenshot('Direct_pay_failed.png')
            raise ValueError('Direct pay failed')

    def loading(self):
        self._loading()


