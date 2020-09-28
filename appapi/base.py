# -*- coding: utf-8 -*-
import requests
import json
from pprint import pprint
from config.site_url import Site
from config.user_info import UserInfo
import logging

logging.basicConfig(level=logging.DEBUG, filename='basic_tools.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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
        logging.debug(f'Login: {r.json()}')
        return r.json()

    # 抓取上下限額(這個暫時用不到了, 目前被拔掉)
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
        # 決定是否儲存, 預設是False
        if save:
            with open(self.env + bank_name + '%s' % body + '.json', 'a', encoding='utf-8') as file:
                print(r.json(), file=file)

    def recharge(self, username: str, bank_type: str, amount: str, login_key: int):

        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            user = UserInfo(username)
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

        # 一般轉卡類
        often_recharge = ['AlipayPdd', 'WeiXinPdd', 'AlipayH5', 'WapBank', 'WeiXinScan']

        # 被調用後傳入的銀行類型參數若在常用參數內
        if bank_type in often_recharge:
            url = site.recharge()
            content_type = 'application/x-www-form-urlencoded'
            payload = {'serviceTypeName': bank_type,
                       'amount': amount}
        # 如果輸入的參數都不在常見的充值項目裡, 表示我使用轉卡類, 並對轉卡類不同的request header做區分
        else:
            url = site.recharge_by_bank(bank_type)
            content_type = 'application/json; charset=utf-8'
            if bank_type == 'bank':
                payload = {"MoneyInType": 0, "paytype": 2, "amount": amount}
                payload = json.dumps(payload)
            elif bank_type == 'alipay_bank':
                payload = {"ReferUserName": "", "Amount": amount}
                payload = json.dumps(payload)
            elif bank_type == 'wechat_bank':
                payload = {"userName": "", "amount": amount}
                payload = json.dumps(payload)
            else:
                raise ValueError('Should not input without bank type')

        headers = {
            'Content-Type': content_type,
            'X-Hec-Authentication': login_key,
            'UserID': user.id(),
            'UserName': user.username(),
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/3.12.0'
        }

        r = self.s.post(url, headers=headers, data=payload)

        # 如果輸入的參數都不在常見的充值項目裡, 表示我使用轉卡類且也不用再get json()['Url']
        if bank_type not in often_recharge:
            try:
                logging.debug(r.json())
            except Exception as e:
                raise ValueError(e)
            return r.json()
        elif r.json()['IsSuccess'] is False:
            logging.debug(r.json())
            return r.json()
        # 這裡是常用的充值類別, 且需要get post出去的response url
        else:
            try:
                logging.debug(r.json()['Url'])
            except:
                raise ValueError(f'Can not found the Url in response: {r.json()}')
                # print(f'Recharge: {r.json()}')

            # 拿到充值之後要開啟的頁面並get, 才會把單子打到Apollo
            try:
                get = self.s.get(r.json()['Url'])
                logging.debug(f'Recharge get: {get}')
            except:
                raise ValueError(f'Failed to get url: {r.json()}')

        return r.json()

    # io = input or output(這些參數是預設值, 可以在不用輸入參數時還能用)
    def transfer(self, io='in', game='LC', amount=10, key='123'):
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            if io == 'in':
                url = site.transfer_in(game)
            elif io == 'out':
                url = site.transfer_out(game)
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

        user = UserInfo('wade13')

        headers = {'X-Hec-Authentication': key,
                   'UserID': user.id(),
                   'UserName': user.username()}

        param = {'amount': amount}

        try:
            r = self.s.post(url, headers=headers, params=param, verify=False)
            if r.json()['success']:
                pass
            else:
                raise ValueError('Post failed by transfer')
        except Exception as e:
            raise ValueError(f'Transfer {io} Error: {e}\nGame: {game}')

    # Get 我的餘額
    def get_balance(self, username, time, key) -> 'third game and my balance':
        if self.env == 'sit' or self.env == 'uat':
            site = Site(self.env)
            url = site.get_account_balance()

            user = UserInfo(username)
        else:
            raise EnvironmentError("You can't input without sit or uat. Your input: " + self.env)

        headers = {
            'X-Hec-Authentication': key,
            'UserID': user.id(),
            'UserName': user.username(),
            'User-Agent': 'okhttp/3.12.0',
            'OS': 'iOS',
            'DeviceName': 'iPhone X',
            'SysVersion': '12.1.4',
        }
        param = {'v': time}
        try:
            r = self.s.get(url, headers=headers, params=param)
        except Exception as e:
            raise ValueError(f'Get balance error: {e}')

        third_game_balance = {}

        # print(f'Try: {r.json()["data"]}')
        my_balance = r.json()['data']['AvailableScores']

        for k, v in r.json()['data'].items():
            if 'Avaliable' in k:
                third_game_balance[k] = v

        print(f'The third game balance: {third_game_balance}\nMy balance: {my_balance}')

        return third_game_balance, my_balance


if __name__ == '__main__':
    case = Base('sit')
    response = case.login('jackson')
    case.recharge('jackson', 'bank', '10', response['data']['key'])
    # json = case.login('wade13')
    # case.transfer(io='out', key=json['data']['key'])
