# -*- coding: utf-8 -*-
from base import Base
import os


class GetRange(Base):

    def _login(self):
        self.login()

    def card_only_for_WapBank_Alipay_WeiXin(self, bank_type='WapBank', save=True):
        self.get_money_range('card', bank_type, save)

    def scan_should_input_the_first_blank_and_wechat_only(self, save=True):
        self.get_money_range('wechat', save)

    def h5_only_for_alipay_bank_and_the_second_blank_is_integer(self, bank_type, save=True):
        self.get_money_range(bank_type, 10, save)


# class Recharge(Base):
#
#     def


if __name__ == '__main__':
    case = GetRange('sit', 'wade13', '87604')
    case._login()
    os.chdir('json')
    # case.card_only_for_WapBank_Alipay_WeiXin('Alipay')
    # case.scan_should_input_the_first_blank_and_wechat_only()
    case.h5_only_for_alipay_bank_and_the_second_blank_is_integer('bank')

