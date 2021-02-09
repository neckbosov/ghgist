import os

from ghgist import commands


def test_create_one_and_delete(cmd: commands.Commands):
    """Simple scenario of usage."""
    gist_id = cmd.gist_create('setup.cfg')
    assert len(cmd.gist_list()) == 1
    cmd.gist_delete(gist_id)


def test_empty(cmd: commands.Commands):
    """Get zero gists."""
    assert not len(cmd.gist_list())


def test_download(cmd: commands.Commands):
    """Test dowmload source of gist."""
    gist_id = cmd.gist_create('setup.cfg')
    with open('setup.cfg', 'r') as setup_file:
        source = setup_file.read()
    cmd.gist_download(gist_id, 'setupkek.cfg')
    with open('setupkek.cfg', 'r') as setupkek_file:
        sourcekek = setupkek_file.read()
    assert sourcekek == source
    os.remove('setupkek.cfg')
    cmd.gist_delete(gist_id)


def test_update(cmd: commands.Commands):
    """Update test."""
    gist_id = cmd.gist_create('setup.cfg')
    gist_id = cmd.gist_update(gist_id, 'pyproject.toml')
    with open('pyproject.toml', 'r') as setup_file:
        source = setup_file.read()
    cmd.gist_download(gist_id, 'setupkek.toml')
    with open('setupkek.toml', 'r') as setupkek_file:
        sourcekek = setupkek_file.read()
    assert sourcekek == source
    os.remove('setupkek.toml')
    cmd.gist_delete(gist_id)
