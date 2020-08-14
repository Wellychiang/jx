class Element:

    login_page = {'account': "//*[@placeholder='帐号']",
                  'password': "//*[@placeholder='密码']",
                  'sign_in_button': "//form[@id='formLogin']//input[@value='登  录']"}

    home_page = {'balance': "//*[@id='divHomeBalance']//div[1]/div[2]/span[2]",
                 'deposit': "//*[contains(text(),'充值')]",
                 'mouse_on_money': "//*[@class='btn_dropdown']"}

    deposit_page = {'input_money': "//*[@id='amount']",
                    'quick_recharge': "//*[@id='btnJump']",
                    'recharge_not_visible': "//div[@style='display: none;']//span[contains(text(),'充值金额')]"}
