import pytest
from StringIO import StringIO

from checkout import price
from checkout import Transaction


@pytest.fixture
def catalog():
    return {
        'apple': price.static(100),
        'orange': price.buy_n_get_m_free(100, 2, 1),
        'happiness': price.daily_special(1000, 3, 0.50),
        'ennui': price.cheap_after_dinner(1000, 50, 18),
    }


@pytest.fixture
def checkout(catalog):
    return Transaction(catalog)


def test_single_item(checkout):
    # execute
    checkout.add_purchase('apple')
    r = checkout.total()

    # assert
    assert r.keys() == ['apple']
    assert r['apple'].count == 1


def test_out_of_order_items(checkout):
    # execute, also testing file-like input
    checkout.add_purchases(StringIO('orange\napple\norange\n'))
    r = checkout.total()

    # assert
    assert r.keys() == ['apple', 'orange'] or r.keys() == ['orange', 'apple']
    assert r['apple'].count == 1
    assert r['orange'].count == 2
    assert r['orange'].total_price == 200


def test_multiple_totals(checkout):
    # execute
    checkout.add_purchase('orange')
    checkout.add_purchase('apple')
    checkout.add_purchase('orange')
    r = checkout.total()
    assert r['orange'].count == 2
    checkout.add_purchase('orange')
    r = checkout.total()

    # assert
    assert r.keys() == ['apple', 'orange'] or r.keys() == ['orange', 'apple']
    assert r['apple'].count == 1
    assert r['orange'].count == 3
    assert r['orange'].total_price == 200
