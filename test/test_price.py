import pytest
from datetime import datetime
from mock import patch, Mock
from zope.interface.verify import verifyObject

from checkout import price
from checkout.interface import IPricer


def test_ipricer():
    # verifyObject throws if there's a problem
    verifyObject(IPricer, price.cheap_after_dinner(0, 0, 0))
    verifyObject(IPricer, price.static(100))
    verifyObject(IPricer, price.daily_special(0, 0, 0))
    verifyObject(IPricer, price.buy_n_get_m_free(2, 1, 0))
    # XXX could mark.parametrize this too


@patch('checkout.price.datetime')
def test_dinner_pricer_after(dt):
    # setup
    p = price.cheap_after_dinner(100, 50, 22)
    dt.today.return_value = datetime(2014, 11, 29, 23, 0, 0)
    # 23 hours is after 22 hours, so we should get the after-dinner price

    # execute
    (peritem, total) = p(count=1)

    # assert
    assert total == 50
    assert peritem == total


@patch('checkout.price.datetime')
def test_dinner_pricer_before(dt):
    # setup
    p = price.cheap_after_dinner(100, 50, 18)
    dt.today.return_value = datetime(2014, 11, 29, 14, 0, 0)
    # 14 hours is before 18 hours, so we should get the before-dinner price

    # execute
    (peritem, total) = p(count=1)

    # assert
    assert total == 100
    assert peritem == total


def test_dinner_pricer_error():
    with pytest.raises(RuntimeError):
        price.cheap_after_dinner(100, 50, 24)


@patch('checkout.price.datetime')
def test_daily_special_on_day(dt):
    p = price.daily_special(100, 0, 0.50)  # 50% off mondays
    dt.today.return_value = datetime(2014, 11, 24, 14, 0, 0)
    # november 24, 2014 is a monday

    (peritem, total) = p(count=1)

    assert total == 50
    assert peritem == total


@patch('checkout.price.datetime')
def test_daily_special_off_day(dt):
    p = price.daily_special(100, 1, 0.50)  # 50% off tuesdays
    dt.today.return_value = datetime(2014, 11, 24, 14, 0, 0)
    # november 24, 2014 is a monday

    (peritem, total) = p(count=1)

    assert total == 100
    assert peritem == total


def test_buy_n_error():
    with pytest.raises(RuntimeError):
        price.buy_n_get_m_free(100, 1, 2)


@pytest.mark.parametrize(
    "count,expected_total,msg", [
        (1, 100, 'no savings (total $1)'),
        (2, 200, 'bought 2, 1 is free -- but they only wanted 2. so $2'),
        (3, 200, 'bought 3, so 1 of them is free. $2'),
    ]
)
def test_buy_two_get_one_free(count, expected_total, msg):
    # setup
    pricer = price.buy_n_get_m_free(100, 2, 1)

    # execute
    total = pricer(count=count)[1]

    # assert
    assert total == expected_total, msg


@pytest.mark.parametrize(
    "count,expected_total,msg", [
        (1, 100, ''),
        (2, 200, ''),
        (3, 300, ''),
        (4, 400, ''),
        (5, 500, ''),
        (6, 500, ''),
        (7, 500, ''),
    ]
)
def test_buy_5_get_2_free(count, expected_total, msg):
    # setup
    pricer = price.buy_n_get_m_free(100, 5, 2)

    # execute
    total = pricer(count=count)[1]

    # assert
    assert total == expected_total, msg
