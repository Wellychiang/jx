# -*- coding: utf-8 -*-
import requests
import json
from pprint import pprint
from .site_url import Site

import time
from datetime import datetime


class Base:

    s = requests.session()

    def __init__(self, env='sit', user='wade13', user_id='87604'):
        self.env = env
        self.user = user
        self.id = user_id

    def login(self):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            url = site.login()
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

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

        r = self.s.post(url, headers=headers, data=payload, verify=False)
        print(r)

    def get_money_range(self, bank_name, body=None, save=False):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            url = site.get_money_range(bank_name)
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

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
                print(r.json(), file=file)

    def recharge(self, bank_type: str, amount: float):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            url = site.recharge()
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

        payload = {'serviceTypeName': bank_type,
                   'amount': amount}
        # text / plain
        # application/x-www-form-urlencoded
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Hec-Authentication': '166223ef05ba47b295c921c2d5e7fdaf',
            'UserID': self.id,
            'UserName': self.user
        }

        r = self.s.post(url, headers=headers, data=payload)
        print(r.json())

        get = self.s.get(r.json()['Url'])
        print(get)

    def transfer(self, io='in', game='LC', amount=10):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            if io == 'in':
                url = site.transfer_in(game)
            elif io == 'out':
                url = site.transfer_out(game)

            headers = {'X-Hec-Authentication': '76add206d3474e17b556e39bd5a1eb42',
                       'UserID': self.id,
                       'UserName': self.user,}

            param = {'amount': amount}

            r = self.s.post(url, headers=headers, params=param, verify=False)
            # print(f'user: {self.user} response: {r.json()}')

    def get_balance(self, time):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            url = site.get_account_balance()
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

        headers = {
            'X-Hec-Authentication': 'cd41175a2583440fa2a0ae1fba235869',
            'UserID': self.id,
            'UserName': self.user,
            'User-Agent': 'okhttp/3.12.0',
        }
        param = {'v': time}
        r = self.s.get(url, headers=headers, params=param)
        # print(r.json())

        third_game_balance = {}
        my_balance = r.json()['data']['AvailableScores']

        for k, v in r.json()['data'].items():
            if 'Avaliable' in k:
                third_game_balance[k] = v

        return third_game_balance, my_balance


if __name__ == '__main__':
    case = Base('sit')
    case.login()
    # case.recharge('AlipayScan', 15)


    '''
    轉帳
    '''
    # games = ['LC', 'IM', 'RG', 'IMPP', 'IMPT', 'IMSport', 'IMeBet', 'IMBG']
    # io = 'out'
    #
    # [case.transfer(io, game, 1) for game in games]
    ba = case.get_balance((time.time() * 1000))
    print(ba)

