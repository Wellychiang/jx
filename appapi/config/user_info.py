class UserInfo:

    user_item = {'wade01': {'userid': '73613',
                            'username': 'wade01'},
                 'wade02': {'userid': '73614',
                            'username': 'wade02'},
                 'wade03': {'userid': '73616',
                            'username': 'wade03'},
                 'wade04': {'userid': '73617',
                            'username': 'wade04'},
                 'wade13': {'userid': '87604',
                            'username': 'wade13'},
                 'wade12': {'userid': '87603',
                            'username': 'wade12'},
                 'jackson': {'userid': '69778',
                             'username': 'jackson'},}

    def __init__(self, user):
        self.user = user

    def id(self):
        return self.user_item[self.user]['userid']

    def username(self):
        return self.user_item[self.user]['username']

    def key(self):
        return self.user_item[self.user]['key']
