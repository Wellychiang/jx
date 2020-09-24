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
    check.equal(json['data']['userID'], int(user.id()))


def test_login_success(base):
    username = ['wade12', 'wade13', 'wade01']
    [login_success(base, user) for user in username]


# def test_login_userid_failed(base, ):
#     json = base.login('wade13')
