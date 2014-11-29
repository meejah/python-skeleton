class Purchase(object):
    '''
    Represents the purchase of 1 or more items within a single
    transaction.

    If item_price is None, that's because it doesn't
    make sense for this item's pricing rules. total_price is
    always available, expressed in cents.
    '''

    def __init__(self, name, count, item_price, total_price):
        self.name = name
        """What this product is called."""

        self.count = count
        """How many are being purchased in this transaction."""

        self.item_price = item_price
        """The individual item price (might be None, in cents)."""

        self.total_price = total_price
        """The total price for this transaction (cents)."""
