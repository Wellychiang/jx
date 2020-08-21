class Site:
    sit = "http://www.sit.n51plus.ark88.local/"
    uat = "https://web.6j71.com/"

    #  Login scope
    login = 'Account/LogOn?ReturnUrl='
    login_validate = 'LoginValidate'
    login_index = 'Home/Index'

    add_low_user = 'Account/AddLowUser'

    #  Recharge scope
    recharge = 'Recharge/RechargeToApollo'

    #  Withdraw_scope
    withdraw = "Account/QuickWithdraw"

    balance = 'Home/BalanceInfo'

    login_page = {'sit': {'login': sit + login,
                          'login_validate': sit + login_validate,
                          'login_index': sit + login_index,
                          'add_low_user': sit + add_low_user},
                  'uat': {'login': uat + login,
                          'login_validate': uat + login_validate,
                          'login_index': uat + login_index,
                          'add_low''_user': uat + add_low_user}}

    recharge_page = {'sit': sit + recharge,
                     'uat': uat + recharge}

    withdraw_page = {'sit': sit + withdraw,
                     'uat': uat + withdraw}

    get_balance = {'sit': sit + balance,
                   'uat': uat + balance}

    def __init__(self, site):
        self.site = site

    def login(self, name):
        return self.login_page[self.site][name]

    def recharge(self):
        return self.recharge_page[self.site]

    def withdraw(self):
        return self.withdraw_page[self.site]

    def balance(self):
        return self.get_balance[self.site]
