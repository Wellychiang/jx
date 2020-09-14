# -*- coding: utf-8 -*- #
from .base import Base
import time
import pytest_check as check


def est_clean():

    base = Base()
    base.login()
    third_game, balance = base.get_balance(time.time() * 1000)

    games = ['LC', 'IM', 'RG', 'IMPP', 'IMPT', 'IMSport', 'IMeBet', 'IMBG']

    for game in games:
        while third_game[game + 'AvaliableScores'] != 0:
            base.transfer('out', game, 1)
            print(third_game[game + 'AvaliableScores'])

    # third_game, balance = base.get_balance(time.time() * 1000)


def test_transfer_in_success_equal_one(username='wade13'):

    base = Base('sit')
    json = base.login(username)
    key = json['data']['key']
    # 目前可轉帳的第三方
    games = ['LC', 'IM', 'RG', 'IMPP', 'IMPT', 'IMSport', 'IMeBet', 'IMBG']

    # 拿轉帳前的主錢包金額
    _, my_balance = base.get_balance(username, time.time() * 1000, key)

    # 主錢包金額減掉可轉帳的個第三方總合
    balance_minus_games_transfer = my_balance - len(games)

    # 轉帳各一塊到可轉入的第三方
    [base.transfer('in', game, 1, key) for game in games]

    # 給轉帳到帳20秒時間
    time.sleep(20)

    # 拿轉入第三方後的第三方、主錢包金額
    third_game_balance, result_balance = base.get_balance(username, time.time() * 1000, key)

    # print(third_game_balance['LCAvaliableScores'], balance_minus_games_transfer, result_balance)
    check.equal(balance_minus_games_transfer, result_balance)

    # 檢查可轉帳的所有第三方是否成功轉帳且顯示正確
    [check.equal(third_game_balance[game + 'AvaliableScores'], 1.0)
     for game in games
     if game + 'AvaliableScores' in third_game_balance]


def test_transfer_out_success_equal_zero(username='wade13'):

    base = Base('sit')
    json = base.login(username)
    key = json['data']['key']
    games = ['LC', 'IM', 'RG', 'IMPP', 'IMPT', 'IMSport', 'IMeBet', 'IMBG']

    _, my_balance = base.get_balance(username, time.time() * 1000, key)
    balance_plus_games_transfer = my_balance + len(games)

    [base.transfer('out', game, 1, key) for game in games]
    time.sleep(20)

    third_game_balance, result_balance = base.get_balance(username, time.time() * 1000, key)

    # print(third_game_balance['LCAvaliableScores'], balance_plus_games_transfer, result_balance)
    check.equal(balance_plus_games_transfer, result_balance)
    [check.equal(third_game_balance[game + 'AvaliableScores'], 0)
     for game in games
     if game + 'AvaliableScores' in third_game_balance]


if __name__ == '__main__':
    pass
