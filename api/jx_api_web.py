import requests
from site_url import Site
from lxml import etree

from pyDes import des, CBC, PAD_PKCS5
import binascii

from pprint import pprint


class Api:

    s = requests.session()

    sit = "http://www.sit.n51plus.ark88.local/"
    uat = "https://web.6j71.com/"

    def __init__(self, env):
        self.env = env

    def login(self, user='wade01', pwd='a111222'):

        if self.env == 'sit' or self.env == 'uat':

            site = Site(self.env)
            url = site.login('login')
            url2 = site.login('login_validate')
            url3 = site.login('login_index')
        else:
            raise ValueError('Can not input without sit or uat, now your input : ' + self.env)

        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Cookie": "PlayTypeIntro=1; UserPlayType=0; DePK10UserPlayType=1; "
                    "HSPK10UserPlayType=1; BeijingPK10UserPlayType=1; g=777abf731810433db0bf7d00b20b339f"}

        data = {"UserName": user,
                "Password": pwd,
                "ValidatorCode": "",
                "isRegist": "false"}

        r = self.s.post(url, headers=headers, data=data)

        print(r.json())

        # validate區
        headers2 = {"Content-Type": "application/x-www-form-urlencoded"}

        data2 = {"url": url2 + "Login",
                 "key": r.json()['key'],
                 "path": ""}

        r = self.s.post(url2, headers=headers2, data=data2, allow_redirects=False)
        print(r)
        cookies = r.headers['Set-Cookie']
        headers3 = {"Cookie": "%s" % cookies}

        # getIndex區
        r2 = self.s.get(url3, headers=headers3)

    def add(self, addname: str, num: int, frequency: int) -> 'freq is for':   # 創建帳號會顯示在 '登入' 帳號底下

        if self.env == 'sit' or 'uat':
            site = Site(self.env)
            url = site.page('add_low_user')
        else:
            raise ValueError('Can not input without sit or uat, now you input is: ' + self.env)

        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

        for i in range(frequency):
            num += 1
            data = {
                "rootUserId": 875252,
                "rootRoleId": 7,
                "rootUserPath": "/0//1//224//229//462//2842//453578//489529//655874//676741/",
                "lowUserName": addname + num,
                "lowUserPwd": "a111222",
                "lowUserRebatePro": 0
            }
            r = self.s.post(url, headers=headers, data=data)
            print(r.json()['message'], '%s%s' % (addname, num))

    # useless
    def recharge_directpay(self, amount: float):
        if self.env == 'sit' or 'uat':
            site = Site(self.env)
            url = site.recharge()
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "37",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "Host": "www.sit.n51plus.ark88.local",
            # "Origin": "http://www.sit.n51plus.ark88.local",
            # "Referer": "http://www.sit.n51plus.ark88.local/Account/Recharge",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",

            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/78.0.3904.108 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        data = {
            "serviceTypeName": "DirectPay",
            "amount": amount
        }
        r = self.s.post(url, headers=headers, data=data)
        print(r)
        return r.json()

    # Not done yet, need to DES hash (userid + & + AdminBankId)
    def recharge_directpayrealname(self, amount: float):
        if self.env == 'sit' or 'uat':
            site = Site(self.env)
            url = site.recharge()

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Content-Length": "37",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Cookie": "PlayTypeIntro=1; UserPlayType=0; DePK10UserPlayType=1; HSPK10UserPlayType=1; "
                      "BeijingPK10UserPlayType=1; Preference_73614_433=73614_433&433=0; __51cke__=; "
                      "ASP.NET_SessionId=mufkwjyaknjw3xbrww5z4jxw; Domain=http%3a%2f%2fwww.sit.n51plus.ark88.local%3a80;"
                      " voice=on; __tins__17709272=%7B%22sid%22%3A%201597374317538%2C%20%22vd%22%3A%201%2C%20%22expire"
                      "s%22%3A%201597376117538%7D; __51laig__=3; UniqueID=0f93bb87-3690-4168-9b36-f5d029b9ef6e; "
                      "g=8b873efc94aa49619e0d0ad0adc63cd0; HECBET=B94413B91655E59869A83A67B1058048789BCAD"
                      "254D79C319870DA44C98E441BE44ABF396884835312834E63D37696C2F8D90B5275E51C663DBD7C8EC"
                      "B66960501F98E96A3EF72D72A6A7C95E22AA690F6629AA3FA1046CF868D7A91E3D5283163C9D487095D"
                      "BDD3C69E19AC407C1787C8520531; Token=B6CD9B07DDB24206EA18A8344EFB852A5985428FF349B1F5"
                      "7248D05FF943852858EA31FBF46E95828158277B614452FE18B7179037F11F649FDF24CB8539956B",
            # "Host": "www.sit.n51plus.ark88.local",
            # "Origin": "http://www.sit.n51plus.ark88.local",
            # "Referer": "http://www.sit.n51plus.ark88.local/Account/Recharge",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",

            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/78.0.3904.108 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }

        data = {
            "serviceTypeName": "DirectPayRealName",
            "amount": amount
        }
        r = self.s.post(url, headers=headers, data=data)
        print(r)
        return r.json()

    def real_name_get(self):
        url = 'http://pay.6j71.com/Pay.aspx'
        a = self.des_encrypt('cpolyhag', 10)
        b = self.des_encrypt('cpolyhag', 69778&4058)
        data = {'Amount': a,
                'Remark': b}

        r = self.get(url, params=data)
        print(r)

    # Done but need to var Bankid,  BankType
    def withdraw(self, amount: int):
        if self.env == 'sit' or 'uat':
            site = Site(self.env)
            url = site.withdraw()

        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

        data = {'BankId': 373423,
                'BankCard': '',
                'BankTypeId': 11,
                "BankName": '上海浦东发展银行',
                'CardUser': '',
                'MoneyPassword': 'a12345',
                'Amount': amount}

        r = self.s.post(url, headers=headers, data=data)
        print(r.json())

    def balance(self, type):
        if self.env == 'sit' or 'uat':
            site = Site(self.env)
            url = site.balance()

        r = self.s.get(url)

        source = etree.HTML(r.text)
        find = source.xpath("//div[contains(@class,'balance_box_con')]//text()")
        balance_list = ''.join(find).split()

        all = {}
        main = -4
        balance = -3
        freeze = -2
        win = -1
        for i in range(12):
            main += 4
            balance += 4
            freeze += 4
            win += 4
            all[balance_list[main]] = [balance_list[balance], balance_list[freeze],
                                       balance_list[freeze], balance_list[win]]

        assert len(all) == 12, 'All balance type is about 12, but now just %s' % len(all)

        btype = {'主帳戶': '主账户', 'ag': 'AG真人转帐', 'ebet': 'eBET真人转帐', 'pt': 'PT电游转帐', 'pp': 'PP电子转帐',
                 '老虎機': '老虎机转帐', 'lc': 'LC棋牌转帐', 'imlc': 'IM棋牌转帐', '沙巴': '沙巴体育转帐',
                 'imsport': 'IM体育转帐', 'rg': 'RG电竞转帐', 'im': 'IM电竞转帐'}

        return all[btype[type]]

    def des_encrypt(self, secret_key, s):
        """
        DES 加密
        :param s: 原始字符串
        :return: 加密后字符串，16进制
        """

        iv = secret_key
        k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        en = k.encrypt(s, padmode=PAD_PKCS5)
        return binascii.b2a_hex(en)


api = Api('uat')

# #
# api.login('wade01')
# # a = api.recharge(10)
# # a = api.recharge_directpayrealname(10)
# type = api.balance('lc')
# print(type)
# # a = api.withdraw(20)
# # api.withdraw(100)


