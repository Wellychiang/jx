# -*- coding: utf-8 -*-
import requests
import json
from pprint import pprint
from site_url import Site


class Base:

    s = requests.session()

    sit = 'http://192.168.3.16:7788'
    uat = ''

    def __init__(self, env='sit', user='wade13', user_id='87604'):
        self.env = env
        self.user = user
        self.id = user_id

    def login(self):
        if self.env == 'sit' or 'uat':
            site = Site(self.env)
            url = site.login()

        headers = {
            'X-Hec-Authentication': 'e0e350090892493da83ff48180f4d3d0',
            'OS': 'iOS',
            'DeviceName': 'iPhone X',
            'SysVersion': '12.1.4'
        }

        payload = {'UserName': self.user,
                   'password': '6c9748a341ae99',
                   'captcha_key': '',
                   'captcha_value': '',
                   'validatorCode': 'KEHT',
                   'nameType': 'account'}

        r = self.s.post(url, headers=headers, data=payload)
        print(r)

    def get_money_range(self, bank_name, body=None, save=False):
        if self.env == 'sit' or 'uat':
            site = Site(self.env)
            url = site.get_money_range(bank_name)

            if type(body) == int:
                content_type = 'text/plain'
                data = {'amount': body}

            elif type(body) == str:  # 轉卡
                cards = ['WapBank', 'Alipay', 'WeiXin']
                if body not in cards:
                    raise ValueError('You can only input ', cards, 'if bank_name is "card"')
                content_type = 'application/json'
                data = {'serviceTypes': [body]}
                data = json.dumps(data)
                print('str')

            else:
                data = None
                content_type = 'text/plain'

            headers = {
                'Content-Type': content_type,
                'X-Hec-Authentication': '166223ef05ba47b295c921c2d5e7fdaf',
                'UserID': self.id,
                'UserName': self.user
            }

            r = self.s.get(url, headers=headers, data=data)
            pprint(r.json()['data'])

            if save:
                with open(self.env + bank_name + '%s' % body + '.json', 'a', encoding='utf-8') as file:
                    print(r.text, file=file)


# base = Base('sit')
# base.login()

"""
# 1. Card only for 'WapBank', 'Alipay', 'WeiXin', Example: ('card', 'WapBank')
# 2. Scan should input the first blank like 'wechat', Example: ('wechat')
# 3. H5 only for 'alipay', 'bank' and the second blank is integer, Example: ('alipay', 10)
"""
# base.get_money_range('card', 'WapBank', True)
# base.get_money_range('wechat', True)
# base.get_money_range('alipay', 10, True)
if __name__ == '__main__':
    pass