from jx_api_web import Api


api = Api('sit')


def test_login():
    try:
        api.login('wade0', 'a111222')
        balance = api.balance('lc')
        if type(balance) != list:
            raise ValueError('Test failed, balance: ' + balance)

    except IndexError as e:
        print('Failed to sign in')

    except Exception as e:
        print(e)

# def
test_login()
