'''
Define the command-line interface using the Click library by Armin Ronacher.
http://click.pocoo.org
'''

# Opinion: I like grouping imports together, and have 3 categories
# usually: standard library; third-party libraries; "local" modules or
# libraries.

from json import dumps

import click

from checkout import Transaction, price

'''
For simplicity, we just statically encode our product catalog here
instead of, e.g., loading it from a file or database or whatever.
'''
catalog = dict(
    apple=price.static(100),  # apples at $1, always
    orange=price.buy_n_get_m_free(100, 2, 1),  # orange $1, buy 2 get 1 free
    happiness=price.daily_special(1000, 3, 0.50),  # 50% off on thursdays!
    ennui=price.cheap_after_dinner(1000, 50, 18),  # change price at 6pm
)


def print_catalog(ctx, param, value):
    '''
    Helper to dump the current catalog.

    Shows how a "click" callback can work (this is for the --catalog
    option).
    '''
    if not value or ctx.resilient_parsing:
        return
    for k in sorted(catalog.keys()):
        click.echo("%20s  %s" % (k, catalog[k].description))
    ctx.exit()


@click.command()
@click.option(
    '--json/--no-json',
    help='Ouput in JSON or not.'
)
@click.option(
    '--catalog',
    help='Output the current catalog.',
    is_flag=True,
    callback=print_catalog,
    expose_value=False,
    is_eager=True
)
def cli(json):
    '''
    Reads items to purchase from STDIN, one per line, and outputs an
    itemized receipt.
    '''
    try:
        co = Transaction(catalog)
        co.add_purchases(click.get_text_stream('stdin'))
        receipt = co.total()

        if json:
            format_json(receipt)
        else:
            format_receipt(receipt)
    except RuntimeError as e:
        click.echo("Error: %s" % e.message)
        exit(1)


def format_json(receipt):
    '''
    Print out the given receipt in JSON.
    '''
    d = dict()
    total = 0
    # XXX could do as dict-comprehension instead?
    for (name, purchase) in receipt.iteritems():
        d[name] = purchase.total_price
        total += purchase.total_price
    d['order_total'] = total
    click.echo(dumps(d))


def format_receipt(receipt):
    '''
    Prints out the given receipt in glorious ASCII
    '''

    order_total = 0
    width = 40
    for (name, purchase) in receipt.iteritems():
        order_total += purchase.total_price
        dots = '.' * (width - len(name))
        price_str = '$%.2f' % (purchase.total_price / 100.0)
        print '%3dx %s %s %8s (%s)' % (purchase.count, name, dots,
                                       price_str, catalog[name].description)
    print ' ' * 47 + '-' * 8

    label = 'Total'
    dots = '.' * (width - len(label) + 5)  # +5 for the quantity "column"
    total_str = '$%.2f' % (order_total / 100.0)
    print '%s %s %8s' % (label, dots, total_str)
