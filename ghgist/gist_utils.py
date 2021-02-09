from typing import Any, Dict


def format_gist(num: int, gist: Dict[str, Any]) -> str:  # type: ignore
    """Create well-formatted string representation of GitHub Gist.

    >>> format_gist(0, {'id': 1,'files':{'kek':''},'url':'https://github.com'})
    '1. <1> kek: https://github.com'
    """
    gist_id: str = gist['id']
    gist_name: str = list(gist['files'].keys())[0]
    gist_link: str = gist['url']
    return '{0}. <{1}> {2}: {3}'.format(num + 1, gist_id, gist_name, gist_link)
