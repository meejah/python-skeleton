'''
This module contains a number of helper functions that instantiate
objects implmenting :class:`checkout.interface.IPricer`

This module is intended to be used like so::

    from checkout import price
    catalog = {
        "apple": price.static(100),
        "orange": price.buy_n_get_m_free(100, 3, 2),
    }

This means apples always cost $1 and oranges are $1 each, but if you
buy 3 you get 2 free.
'''

from datetime import datetime
from zope.interface import directlyProvides, implementer
from interface import IPricer


def static(price):
    '''
    Returns a :class:`checkout.interface.IPricer` with a static price.
    '''

    @implementer(IPricer)
    class StaticPricer(object):
        description = '$%0.2f each' % (price / 100.0)

        def __call__(self, count, **kw):
            return (price, price * count)
    return StaticPricer()


def cheap_after_dinner(price_before, price_after, dinnertime):
    '''
    Returns a :class:`checkout.interface.IPricer` which gives a different
    price after dinnertime.

    :param dinnertime: time for dinner, 0-23 (in hours).
    '''
    if dinnertime < 0 or dinnertime > 23:
        raise RuntimeError("Dinnertime is hours, in 24-hour format.")

    @implementer(IPricer)
    class AfterDinnerPricer(object):
        description = "$%.2f before %02d00 hours, $%.2f after" %\
            (price_before / 100.0, dinnertime, price_after / 100.0)

        def __call__(self, count, **kw):
            if datetime.today().hour >= dinnertime:
                return (price_after, price_after * count)
            return (price_before, price_before * count)

    return AfterDinnerPricer()


def daily_special(price, day_of_week, discount):
    '''
    Returns a :class:`checkout.interface.IPricer` which is discounted a
    certain amount on particular day-of-the-week.

    :param day_of_week: 0-6 (monday through sunday)
    :param discount: percent of discount, 0.0 -> 1.0
    '''
    weekdays = ['mon', 'tue', 'wed', 'thrs', 'fri', 'sat', 'sun']

    @implementer(IPricer)
    class DailySpecialPricer(object):
        description = '$%.2f each, %d%% off %s' % \
            (price / 100.0, (discount * 100), weekdays[day_of_week])

        def __call__(self, count, **kw):
            myprice = price
            if datetime.today().weekday() == day_of_week:
                myprice = int(price * discount)
            return (myprice, myprice * count)

    return DailySpecialPricer()


def buy_n_get_m_free(price, n, m):
    '''
    Returns a :class:`checkout.interface.IPricer` which does (a version
    of) "buy N get M free". For the border-case of wishing to purchase
    fewer than you're entitled to, we opt for "screw the customer",
    basically. Alternatively, we could provide a way to update the
    count to reflect the free items.

    For example, with "buy 5 get 2 free" if you buy 5 things, you
    still pay the same as if you bought 6 or 7.
    '''
    if m >= n:
        raise RuntimeError("Can't buy %d and get %d free." % (n, m))

    # here, we implement the IPricer interface (a Functor pattern) not
    # as a class but as a function directly, to demonstrate
    # zope.interface's "directlyProvides" functionality and a Python
    # closure. Note how we satisfy the "description" attribute by
    # adding it to the method object; that can be done in- or out-side
    # of the inner method.
    def buy_n_pricer(count, **kw):
        groups = count / (n + m)
        leftover = count % (n + m)
        free = groups * m
        paid = (groups * n)
        if leftover > n:
            paid = n
            free = leftover - n
        else:
            paid += leftover
        assert paid + free == count
        total = paid * price
        return (None, total)
    buy_n_pricer.description = 'Buy %d get %d free' % (n, m)
    directlyProvides(buy_n_pricer, IPricer)

    return buy_n_pricer
