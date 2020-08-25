class Site:
    sit = "http://192.168.3.16:7788"
    uat = "https://web.6j71.com/"

    #  Login scope
    login = '/Account/LogOnV1'

    add_low_user = 'Account/AddLowUser'

    #  Recharge scope
    recharge = '/RechargeApollo'
    card = '/GetRechargeInformation/'
    wechat = '/Wechat'
    bank = '/Online'
    alipay = '/AlipayDirect/'



    #  Withdraw_scope
    withdraw = "Account/QuickWithdraw"

    balance = 'Home/BalanceInfo'

    login_page = {'sit': sit + login,
                  'uat': uat + login,}

    recharge_page_get = {'sit': {'wechat': sit + recharge + wechat,
                                 'bank': sit + recharge + bank,
                                 'alipay': sit + recharge + alipay,
                                 'card': sit + recharge + card},
                         'uat': {'wechat': uat + recharge + wechat,
                                 'bank': uat + recharge + bank,
                                 'alipay': uat + recharge + alipay,
                                 'card': uat + recharge + card
                                 }}

    withdraw_page = {'sit': sit + withdraw,
                     'uat': uat + withdraw}

    get_balance = {'sit': sit + balance,
                   'uat': uat + balance}

    def __init__(self, site):
        self.site = site

    def login(self):
        return self.login_page[self.site]

    def get_money_range(self, name):
        return self.recharge_page_get[self.site][name]

    def withdraw(self):
        return self.withdraw_page[self.site]

    def balance(self):
        return self.get_balance[self.site]