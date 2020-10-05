from common import base


class HomePage(base.Base):

    _mouse_on_money = "//*[@class='btn_dropdown']"
    _balance = "//*[@id='divHomeBalance']//div[1]/div[2]/span[2]"
    _deposit = "//*[contains(text(),'充值')]"

    def switch_window(self):
        self._switch_window()

    def mouse_on_money(self):
        try:
            self.find_element(self._mouse_on_money).click()
        except:
            self.sleep(2)
            self.find_element(self._mouse_on_money).click()

    def catch_money(self):
        if self.find_element(self._balance).text.strip('¥') == '':
            self.sleep(2)
            print(self.find_element(self._balance).text)
        else:
            print(self.find_element(self._balance).text)

    def click_to_recharge_page(self):
        self.find_element(self._deposit).click()