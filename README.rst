python-skeleton
===============

This is a skeleton Python command-line project with documentation,
tests (using py.test), distutils support and a few opinions on layout
and styles (marked with ``# Opinion:`` comments in the code).

As example code, it also implements a simple "checkout" system. This
takes a line-by-line list of purchases on stdin and outputs an
itemized receipt on stdout.

Configuration (prices, specials, promotions, etc) is achieved in the
code (``checkout/catalog.py``).

Installation
------------

After cloning the Git repository, you should install this in a
virtualenv and set up for development::

    virtualenv venv
    ./venv/bin/pip install --editable .[dev]

(Or simply ``make venv``). Then, you can try one of the examples::

   cat input_0 | ./venv/bin/checkout

Of course, you can also activate the virtualenv
(``. venv/bin/activate``) giving you ``checkout`` in your ``PATH``. On
a Debian or Ubuntu machine, you'll need to have python, pip and virtualenv
installed first::

   apt-get install python-pip python-virtualenv

All Makefile targets:

  * ``make test``: use `py.test <http://pytest.org>`_ to run unit tests
  * ``make doc``: build documentation using `Sphinx <http://sphinx-doc.org/>`_ (visit docs with ``sensible-browser ./doc/_build/html/index.html``)
  * ``make pep8``: run pep8 on all code
  * ``make venv``: create a virtualenv called ``venv`` (if it's not already there)


  
Usage and Configuration
-----------------------

Simply cat files through the ``checkout`` tool; it reads all of stdin.
To demonstrate usage of `Click <http://click.pocoo.org/>`_ for
command-line options, you may also pass a ``--json`` option to get
JSON-formatted output or ``--catalog`` for a list of all products.

If you want to change the available items or prices, edit the file
``checkout/cli.py`` near the top.


Libraries Used, and Why
-----------------------

`Sphinx <http://sphinx-doc.org/>`_: The de-facto standard Python
documentation system. Uses rST for markup and has several high-quality
themes. See ``doc/*.rst`` and ``README.rst`` for the documentation
you're currently reading.

`Alabaster <https://github.com/bitprophet/alabaster>`_ theme for
Sphinx: a very clean, simple and mobile-friendly theme. Can include
Travis-CI, GitHub etcetera links. See ``doc/conf.py`` for setup.

`Click <http://click.pocoo.org/>`_: a great library for making
command-line interfaces mostly by writing functions and adding
decorators to them. Bash completion support, cross-platform. See
``checkout/cli.py``.

`pytest <http://pytest.org/>`_: I really like the functional style of
this testing library and runner, and the nice support for fixtures and
paramterizing tests. With extensive hooks for customization, using
this is a pleasure. See ``test/*.py`` where I include some simple
fixture and paramterization examples.

`zope.interface <http://docs.zope.org/zope.interface/>`_: not just for
Twisted! Making your duck-typing a little more explicit with
interfaces is nice. ``zope.interface`` also provides some other
goodies. See ``checkout/interface.py`` for a very simple example.
