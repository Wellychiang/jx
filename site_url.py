class Url:
    sit = "http://www.sit.n51plus.ark88.local/"
    uat = "https://web.6j71.com/"

    login = 'Account/LogOn?ReturnUrl='
    login_validate = 'LoginValidate'
    login_index = 'Home/Index'

    add_low_user = 'Account/AddLowUser'

    recharge = 'Recharge/RechargeToApollo'

    data = {'sit': {'login': sit + login,
                    'login_validate': sit + login_validate,
                    'login_index': sit + login_index},

            'uat': {'login': uat + login,
                    'login_validate': sit + login_validate,
                    'login_index': sit + login_index}}

    def __init__(self, site):
        self.site = site

    def url(self, name):
        return self.data[self.site][name]