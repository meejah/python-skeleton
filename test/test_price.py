import pytest
from checkout import price


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
