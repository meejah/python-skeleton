'''
This module implements a simple checkout system.

Prices can change frequently and have arbitrarly complicated rules for
determining an individual item's price.

In-code configuration is achieved with a dict mapping item-names
(strings) to a an object that implements :class:`checkout.interface.IPricer`.
There are helpers in sub-module "price" to aid instantiating these.
'''

# Opinion: a flatter namespace is nice, but it's preferable to have
# classes (or tightly coupled classes or functions) in their own
# files. So, we bring in the indiviual classes to this namespace.
from .purchase import Purchase
from .transaction import Transaction

# ...but we can still provide a sub-namespace, of course
import price
import interface

# FIXME catalog should go elsewhere
catalog = {
    'apple': price.static(100),  # apples at $1, always
    'orange': price.buy_n_get_m_free(100, 2, 1),  # orange $1, buy 2 get 1 free
    'happiness': price.daily_special(1000, 3, 0.50),  # 50% off on thursdays!
    'ennui': price.cheap_after_dinner(1000, 50, 18),  # change price at 6pm
}

# Opinion: to keep our namespace clean, we declare our exports explicitly
__all__ = ['price', 'interface', 'catalog',
           'Transaction', 'Purchase']
