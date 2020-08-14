from appium import webdriver


desired_caps = {'deviceName' : '127.0.0.1:62001',
                    'platformName' : 'android',
                    'appPackage' :'tw.com.ark.football_dev_test',
                    'appActivity' : 'tw.com.ark.football.login.LoginActivity',
                    'noReset' : 'true'}
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(8)