import requests


sit = 'http://192.168.3.16:7788'
uat = ''


class Base:

    s = requests.session()

    def __init__(self, env):
        self.env = env
        if env != 'sit' or 'uat':
            raise EnvironmentError('Can not input without sit or uat, now your input: ' + self.env)

    def login(self):

        url = self.env + '/Account/LogOnV1'
        headers = {
            'X-Hec-Authentication': 'e0e350090892493da83ff48180f4d3d0',
            'OS': 'iOS',
            'DeviceName': 'iPhone X',
            'SysVersion': '12.1.4'
        }

        payload = {'UserName': 'wade13',
                   'password': '6c9748a341ae99',
                   'captcha_key': '',
                   'captcha_value': '',
                   'validatorCode': 'KEHT',
                   'nameType': 'account'}

        r = self.s.post(url, headers=headers, data=payload)
        print(r.json())

    def

