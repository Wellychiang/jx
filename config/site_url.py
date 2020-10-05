class Site:
    sit = "http://192.168.3.16:8082"
    uat = "https://web.6j71.com"

    # Login scope
    login = '/Account/LogOnV1/'
    login_page = {'sit': sit + login,
                  'uat': uat + login,}

    # Recharge scope
    # Get
    basic_apollo = '/RechargeApollo'
    card = '/GetRechargeInformation/'
    wechat = '/Wechat'
    bank = '/Online'
    alipay = '/AlipayDirect/'

    # Post
    basic_post_after_apollo = '/RechargeToApollo/'
    apollo_page = 'http://recharge.sit.n51plus.ark88.local/Pay.aspx'
    recharge = '/recharge/'
    recharge_alipay = 'submitalipayV1'  # 支付寶轉卡(銀行轉帳)
    recharge_bank = 'submitbank'  # 網銀轉帳(銀行轉帳)
    recharge_wechat = 'wechat2'  # 微信轉帳(銀行轉帳)

    recharge_get = {'sit': {'wechat': sit + basic_apollo + wechat,
                            'bank': sit + basic_apollo + bank,
                            'alipay': sit + basic_apollo + alipay,
                            'card': sit + basic_apollo + card,
                            'alibank': sit + recharge + recharge_alipay,
                            'recharge_bank': sit + recharge + recharge_bank},
                    'uat': {'wechat': uat + basic_apollo + wechat,
                            'bank': uat + basic_apollo + bank,
                            'alipay': uat + basic_apollo + alipay,
                            'card': uat + basic_apollo + card,
                            'alibank': uat + recharge + recharge_alipay,
                            'recharge_bank': uat + recharge + recharge_bank
                                 }}
    # 一般充值類
    recharge_post = {'sit': sit + basic_apollo + basic_post_after_apollo,
                     'uat': uat + basic_apollo + basic_post_after_apollo}
    # 轉卡類
    recharge_post_bank = {'sit': {'bank': sit + recharge + recharge_bank,
                                  'alipay_bank': sit + recharge + recharge_alipay,
                                  'wechat_bank': sit + recharge + recharge_wechat},
                          'uat': {'bank': uat + recharge + recharge_bank,
                                  'alipay_bank': uat + recharge + recharge_alipay,
                                  'wechat_bank': uat + recharge + recharge_wechat},
                          }

    # Withdraw_scope
    withdraw = "Account/QuickWithdraw"
    withdraw_page = {'sit': sit + withdraw,
                     'uat': uat + withdraw}

    # Balance
    balance = 'Home/BalanceInfo'
    get_balance = {'sit': sit + balance,
                   'uat': uat + balance}
    '''''''''''
       轉帳區
    '''''''''''
    # Balance
    account_balance = '/account/balance'
    _get_account_balance = {'sit': sit + account_balance,
                            'uat': uat + account_balance}
    # Transfer in
    LC = '/LC/TransferIn'
    IM = '/IM/TransferIn'
    RG = '/RG/TransferIn'
    IMPP = '/IMPP/TransferIn'
    IMPT = '/IMPT/TransferIn'
    IMSport = '/IMSport/TransferIn'
    IMeBet = '/IMeBet/TransferIn'
    IMBG = '/IMBG/TransferIn'

    _transfer_in = {'sit':   {'LC': sit + LC,
                              'IM': sit + IM,
                              'RG': sit + RG,
                              'IMPP': sit + IMPP,
                              'IMPT': sit + IMPT,
                              'IMSport': sit + IMSport,
                              'IMeBet': sit + IMeBet,
                              'IMBG': sit + IMBG,},
                    'uat': {'LC': uat + LC,
                            'IM': uat + IM,
                            'RG': uat + RG,
                            'IMPP': uat + IMPP,
                            'IMPT': uat + IMPT,
                            'IMSport': uat + IMSport,
                            'IMeBet': uat + IMeBet,
                            'IMBG': uat + IMBG,}}

    # Transfer out
    LCOut = '/LC/TransferOut'
    IMOut = '/IM/TransferOut'
    RGOut = '/RG/TransferOut'
    IMPPOut = '/IMPP/TransferOut'
    IMPTOut = '/IMPT/TransferOut'
    IMSportOut = '/IMSport/TransferOut'
    IMeBetOut = '/IMeBet/TransferOut'
    IMBGOut = '/IMBG/TransferOut'

    _transfer_out = {'sit':  {'LC': sit + LCOut,
                              'IM': sit + IMOut,
                              'RG': sit + RGOut,
                              'IMPP': sit + IMPPOut,
                              'IMPT': sit + IMPTOut,
                              'IMSport': sit + IMSportOut,
                              'IMeBet': sit + IMeBetOut,
                              'IMBG': sit + IMBGOut,},
                     'uat':  {'LC': uat + LCOut,
                              'IM': uat + IMOut,
                              'RG': uat + RGOut,
                              'IMPP': uat + IMPPOut,
                              'IMPT': uat + IMPTOut,
                              'IMSport': uat + IMSportOut,
                              'IMeBet': uat + IMeBetOut,
                              'IMBG': uat + IMBGOut,}}

    def __init__(self, site):
        self.site = site

    def login(self):
        return self.login_page[self.site]

    def get_money_range(self, name):
        return self.recharge_get[self.site][name]

    def withdraw(self):
        return self.withdraw_page[self.site]

    def balance(self):
        return self.get_balance[self.site]

    def recharge(self):
        return self.recharge_post[self.site]

    def recharge_by_bank(self, name):
        return self.recharge_post_bank[self.site][name]

    def transfer_in(self, name):
        return self._transfer_in[self.site][name]

    def transfer_out(self, name):
        return self._transfer_out[self.site][name]

    def get_account_balance(self):
        return self._get_account_balance[self.site]