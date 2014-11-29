import json

import pytest
from click.testing import CliRunner

from checkout.cli import cli


def test_cli_checkout():
    result = CliRunner().invoke(cli, [], input='apple\norange\n')

    assert result.exit_code == 0
    assert 'Total' in result.output
    assert '$2.00' in result.output


def test_cli_checkout_json():
    result = CliRunner().invoke(cli, ['--json'], input='apple\norange\n')

    assert result.exit_code == 0
    data = json.loads(result.output)


def test_cli_checkout_error():
    result = CliRunner().invoke(cli, [], input='a vague feeling of remorse\n')

    assert result.exit_code != 0
    assert 'Error' in result.output


def test_cli_catalog():
    result = CliRunner().invoke(cli, ['--catalog'])

    assert result.exit_code == 0
    from checkout.cli import catalog
    for product in catalog.keys():
        assert product in result.output
