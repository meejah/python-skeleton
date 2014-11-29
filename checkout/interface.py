from zope.interface import Interface


class IPricer(Interface):
    def __call__(self, **kwargs):
        '''Currently, only "count" may exist in the kwargs. This is how many
        of the current item are being purchased in the current
        transaction.

        This method should return a 2-tuple: the per-item price in
        cents, expressed as an integer followed by the total price
        (cents, as integer).
        '''
