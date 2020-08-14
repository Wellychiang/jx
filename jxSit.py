import requests
import site_url

s = requests.session()

sit = "http://www.sit.n51plus.ark88.local/"
uat = "https://web.6j71.com/"


def login(user='wade01', pwd='a111222', env='uat'):

    if env == 'sit':
        # url = "%sAccount/LogOn?ReturnUrl=" % sit
        # url2 = "%sLoginValidate" % sit
        # url3 = "%sHome/Index" % sit
        # datasUrl = sit
        url = site_url('sit')

    elif env == 'uat':
        # url = "%sAccount/LogOn?ReturnUrl=" % uat
        # url2 = "%sLoginValidate" % uat
        # url3 = "%sHome/Index" % uat
        # datasUrl = uat
        url = site_url('uat')

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "PlayTypeIntro=1; UserPlayType=0; DePK10UserPlayType=1; "
                  "HSPK10UserPlayType=1; BeijingPK10UserPlayType=1; g=777abf731810433db0bf7d00b20b339f"
    }

    data = {
        "UserName": "%s" % user,
        "Password": "%s" % pwd,
        "ValidatorCode": "",
        "isRegist": "false"
    }

    r = s.post(url.login, headers=headers, data=data)

    print(r.json())

    # validate區
    headers2 = {"Content-Type": "application/x-www-form-urlencoded"}

    data2 = {
        "url": url.login_validate + "Login",
        "key": r.json()['key'],
        "path": ""
    }

    r = s.post(url.login_validate, headers=headers2, data=data2, allow_redirects=False)
    print(r)
    cookies = r.headers['Set-Cookie']
    headers3 = {
        "Cookie": "%s" % cookies
    }

    # getIndex區
    r2 = s.get(url.login_index, headers=headers3)
    print(r2)


def add(addname='wade', num=0, frequency=1, env='uat'):   # 創建帳號會顯示在wade01底下
    url = "%sAccount/AddLowUser" % sit if env == 'sit' else "%sAccount/AddLowUser" % uat
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    for i in range(frequency):
        num += 1
        data = {
            "rootUserId": 875252,
            "rootRoleId": 7,
            "rootUserPath": "/0//1//224//229//462//2842//453578//489529//655874//676741/",
            "lowUserName": "%s%s" % (addname, num),
            "lowUserPwd": "a111222",
            "lowUserRebatePro": 0
        }
        r = s.post(url, headers=headers, data=data)
        print(r.json()['message'], '%s%s' % (addname, num))


# UAT SIT還沒分離完
def recharge(env: str, amount: float):
    url = '%sRecharge/RechargeToApollo' % sit if env == 'sit' else '%sRecharge/RechargeToApollo' % uat
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "Content-Length": "37",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "www.sit.n51plus.ark88.local",
        "Origin": "http://www.sit.n51plus.ark88.local",
        "Referer": "http://www.sit.n51plus.ark88.local/Account/Recharge",
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
    r = s.post(url, headers=headers, data=data)
    print(r)
    return r.json()


login(user='wade02', env='sit')
# add('eric0', 0, 1, env='sit')
withdra = recharge('sit', 2000)
print(withdra)


