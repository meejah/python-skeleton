# This is here for convenience and to document how to do certain
# common tasks. For example, type "make venv" or "make test"
.PHONY: test pep8 doc
default: test pep8

venv:
	virtualenv venv
# the .[dev] syntax means "install this thing, with dev extras"
	./venv/bin/pip install --editable .[dev]

doc:
	cd doc && make html

pep8: venv
	./venv/bin/pep8 checkout/*.py test/*.py setup.py

test: venv
	./venv/bin/py.test --verbose --cov checkout --cov-report term-missing test/*.py

coverage: venv
	./venv/bin/py.test --verbose --cov checkout --cov-report html test/*.py
