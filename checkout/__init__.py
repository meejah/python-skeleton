'''
This module implements a simple checkout system.

Prices can change frequently and have arbitrarly complicated rules for
determining an individual item's price.

In-code configuration is achieved with a dict mapping item-names
(strings) to a an object that implements IPricer. There are helpers in
sub-module "price" to aid instantiating these.
'''

import price
import interface

# FIXME XXX move code to individual files

# FIXME catalog should go elsewhere
catalog = {
    'apple': price.static(100),  # apples at $1, always
    'orange': price.buy_n_get_m_free(100, 2, 1),  # orange $1, buy 2 get 1 free
    'happiness': price.daily_special(1000, 3, 0.50),  # 50% off on thursdays!
    'ennui': price.cheap_after_dinner(1000, 50, 18),  # change price at 6pm
}


class Purchase(object):
    '''
    Represents the purchase of 1 or more items within a single
    transaction. If item_price is None, that's because it doesn't
    make sense for this item's pricing rules. total_price is
    always available, expressed in cents.
    '''

    def __init__(self, name, count, item_price, total_price):
        self.name = name
        self.count = count
        self.item_price = item_price
        self.total_price = total_price


class Transaction(object):
    '''
    Represents a single trip to the checkout, encapsulating some
    current pricing rules.
    '''

    def __init__(self, rules):
        '''
        :param rules: the current pricing rules
        '''
        self.rules = rules
        self.purchases = {}  # item name -> count

    def add_purchases(self, filelike):
        '''
        Add purchases from a file, by reading each line and treating it as
        a product name.
        '''
        for line in filelike.readlines():
            line = line.strip()
            if len(line):
                self.add_purchase(line)

    def add_purchase(self, name):
        '''
        Add one more item to this order.
        '''
        name = name.strip().lower()
        if name not in self.rules:
            raise RuntimeError('No such product "%s".' % name)

        self.purchases[name] = self.purchases.get(name, 0) + 1

    def total(self):
        '''
        Returns a dict mapping item name -> Purchase instance

        Note this may be called multiple times. For example, you could
        add several items, call total() (perhaps to display "order so
        far"), add more items and call total() again etc.
        '''

        order = dict()
        for (name, count) in self.purchases.iteritems():
            (per_item, total) = self.rules[name](count=count)
            order[name] = Purchase(name, count, per_item, total)
        return order


# Opinion: to keep our namespace clean, we declare our exports explicitly
# __all__ = ['price', 'catalog',
#           'Transaction', 'format_receipt']
