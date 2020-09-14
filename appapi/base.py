# -*- coding: utf-8 -*-
import requests
import json
from pprint import pprint
from .config.site_url import Site
from .config.user_info import UserInfo


import time


class Base:

    s = requests.session()

    def __init__(self, env='sit'):
        self.env = env

    def login(self, user, pwd='6c9748a341ae99'):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            url = site.login()
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

        headers = {
            'X-Hec-Authentication': 'e0e350090892493da83ff48180f4d3d0',
            'OS': 'iOS',
            'DeviceName': 'iPhone X',
            'SysVersion': '12.1.4',
        }

        payload = {'UserName': user,
                   'password': pwd,
                   'captcha_key': '',
                   'captcha_value': '',
                   'validatorCode': 'RPEU',
                   'nameType': 'account'}

        r = self.s.post(url, headers=headers, data=payload, verify=False)
        print(f'Login: {r.json()}')
        return r.json()

    # 這個暫時用不到了
    def get_money_range(self, bank_name, body=None, save=False):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            url = site.get_money_range(bank_name)

            user = UserInfo('wade01')

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

        else:
            data = None
            content_type = 'text/plain'

        headers = {
            'Content-Type': content_type,
            'X-Hec-Authentication': '166223ef05ba47b295c921c2d5e7fdaf',
            'UserID': user.id(),
            'UserName': user.username()
        }

        r = self.s.get(url, headers=headers, data=data)
        pprint(f"Get money range: {r.json()['data']}")

        if save:
            with open(self.env + bank_name + '%s' % body + '.json', 'a', encoding='utf-8') as file:
                print(r.json(), file=file)

    def recharge(self, username: str, bank_type: str, amount: float, login_key: int):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            url = site.recharge()

            user = UserInfo(username)
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

        payload = {'serviceTypeName': bank_type,
                   'amount': amount}
        # text / plain
        # application/x-www-form-urlencoded
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Hec-Authentication': login_key,
            'UserID': str(user.id()),
            'UserName': user.username(),
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.0'
        }

        r = self.s.post(url, headers=headers, data=payload)
        try:
            r.json()['Url']
        except:
            raise ValueError(f'Can not found the Url in response: {r.json()}')
            # print(f'Recharge: {r.json()}')

        # 拿到充值之後要開啟的頁面並get, 才會把單子打到Apollo

        get = self.s.get(r.json()['Url'])
        print(f'Recharge get: {get}')

    def transfer(self, io='in', game='LC', amount=10):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            if io == 'in':
                url = site.transfer_in(game)
            elif io == 'out':
                url = site.transfer_out(game)
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

        user = UserInfo('wade13')

        headers = {'X-Hec-Authentication': '76add206d3474e17b556e39bd5a1eb42',
                   'UserID': user.id(),
                   'UserName': user.username()}

        param = {'amount': amount}

        try:
            r = self.s.post(url, headers=headers, params=param, verify=False)
        except Exception as e:
            raise ValueError(f'Transfer {io} Error: {e}\nGame: {game}')

    def get_balance(self, username, time) -> 'third game and my balance':
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            url = site.get_account_balance()

            user = UserInfo(username)
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

        headers = {
            'X-Hec-Authentication': 'cd41175a2583440fa2a0ae1fba235869',
            'UserID': user.id(),
            'UserName': user.username(),
            'User-Agent': 'okhttp/3.12.0',
        }
        param = {'v': time}
        try:
            r = self.s.get(url, headers=headers, params=param)
        except Exception as e:
            raise ValueError(f'Get balance error: {e}')

        third_game_balance = {}
        my_balance = r.json()['data']['AvailableScores']

        for k, v in r.json()['data'].items():
            if 'Avaliable' in k:
                third_game_balance[k] = v

        print(f'The third game balance: {third_game_balance}\nMy balance: {my_balance}')

        return third_game_balance, my_balance


if __name__ == '__main__':
    case = Base('sit')
    case.login()
