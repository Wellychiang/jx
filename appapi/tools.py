# -*- coding: utf-8 -*-
from base import Base


class SomeCase(Base):

    def __init__(self, env='sit', user='wade13', user_id='87604'):
        self.env = env
        self.user = user
        self.id = user_id
        self.login()

    def card_only_for_WapBank_Alipay_WeiXin(self, card='card', bank_type='WapBank', save=True):
        self.get_money_range(card, bank_type, save)

    def scan_should_input_the_first_blank_like_wechat(self, save=True):
        self.get_money_range('wechat', save)

    def h5_only_for_alipay_bank_and_the_second_blank_is_integer(self, bank_type, save=True):
        self.get_money_range(bank_type, 10, save)


if __name__ == '__main__':
    case = SomeCase()
    # case.card_only_for_WapBank_Alipay_WeiXin(bank_type='WeiXin')
    # case.h5_only_for_alipay_bank_and_the_second_blank_is_integer('alipay')
    case.scan_should_input_the_first_blank_like_wechat()

