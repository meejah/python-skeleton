import re
from setuptools import setup


def pip_to_requirements(s):
    """
    Change a PIP-style requirements.txt string into one suitable for setup.py
    """

    if s.startswith('#'):
        return ''
    m = re.match('(.*)([>=]=[.0-9]*).*', s)
    if m:
        return '%s (%s)' % (m.group(1), m.group(2))
    return s.strip()


setup(
    name='checkout',
    version=open('VERSION', 'r').read().strip(),
    author='meejah',
    author_email='meejah@meejah.ca',
    license='MIT',
    url='https://github.com/meejah/python-skeleton',

    install_requires=open('requirements.txt').readlines(),
    extras_require=dict(
        dev=open('requirements-dev.txt').readlines()
    ),

    description='XXX Skeleton python project example.',
    long_description=open('README.rst', 'r').read(),
    keywords=['python', 'XXX'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

    packages=["checkout"],
    data_files=[('share/checkout', ['README.rst'])],
    entry_points=dict(
        console_scripts=[
            'checkout=checkout.cli:cli'
        ]
    ),
)
