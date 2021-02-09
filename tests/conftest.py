import json

import pytest

from ghgist import commands


@pytest.fixture
def cmd() -> commands.Commands:
    """Produce Commands object with correct api headers."""
    try:
        with open('.ghgist', 'r') as ghgist_file:
            token = json.load(ghgist_file)['ghgist']['settings']['token']
    except KeyError:
        print('Please store Github access token in correct format')  # noqa: 421
        raise KeyError

    return commands.Commands({
        'Authorization': 'token {0}'.format(token),
        'Accept': 'Accept: application/vnd.github.v3+json',
    })
