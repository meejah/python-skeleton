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
