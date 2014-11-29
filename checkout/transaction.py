from .purchase import Purchase


class Transaction(object):
    '''
    Represents a single trip to the checkout, encapsulating some
    current pricing rules.
    '''

    def __init__(self, rules):
        self.rules = rules
        '''Pricing rules for this transaction.'''

        self.purchases = {}
        '''dict: item name -> count'''

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
