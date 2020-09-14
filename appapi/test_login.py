from .base import Base
from .config.user_info import UserInfo
import pytest_check as check
import pytest


@pytest.fixture()
def base():
    init = Base()
    yield init


def login_success(base, username='wade01'):
    user = UserInfo(username)
    json = base.login(username)

    check.equal(json['message'], '登录成功！')
    check.equal(json['success'], True)
    check.equal(json['data']['userName'], username)
    check.equal(json['data']['userID'], user.id())

# def test_login_userid_failed(base, ):
#     json = base.login('wade13')


def test_login_success(base):
    usernames = ['wade01', 'wade12', 'wade13']
    [login_success(base, username) for username in usernames]
