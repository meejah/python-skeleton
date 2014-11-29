from zope.interface import Interface, Attribute


class IPricer(Interface):
    description = Attribute('A human-readable summary of the pricing scheme.')

    def __call__(count, **kwargs):
        '''
        This method should return a 2-tuple: the per-item price in cents,
        expressed as an integer followed by the total price (cents, as
        integer). The per-item price may be None if that doesn't make
        sense.

        :param count: Number of the current item are being purchased
        in the current transaction.

        '''
