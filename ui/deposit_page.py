from base import Base


class DepositPage(Base):

    _input_amount = "//*[@id='amount']"
    _quick_recharge = "//*[@id='btnJump']"
    recharge_not_visible = "//div[@style='display: none;']//span[contains(text(),'充值金额')]"

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
