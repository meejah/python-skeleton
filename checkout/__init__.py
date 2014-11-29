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

# Opinion: to keep our namespace clean, we declare our exports explicitly
__all__ = ['price', 'interface', 'Transaction', 'Purchase']
