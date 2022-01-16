import json
from typing import Any, Dict, List

import requests
from ghgist import gist_utils

GITHUB_API = 'https://api.github.com'


class Commands(object):
    """Commands for manipulatins GitHub Gists."""

    api_headers: Dict[str, str]

    def __init__(self, headers: Dict[str, str]) -> None:
        """Initialize Commands with given headers for API access."""
        self.api_headers = headers

    def gist_create(self, filename: str) -> str:
        """Create Gist from given file.

        Parameters
        -----------
        filename
            Name of file with content for Gist

        Returns
        -------
        ID of new gist
        """
        with open(filename, 'r') as gist_file:
            gist = {
                'description': '',
                'public': True,
                'files': {
                    filename: {
                        'content': gist_file.read(),
                    },
                },
            }
            url = '{0}/gists'.format(GITHUB_API)
            response = requests.post(
                url,
                headers=self.api_headers,
                data=json.dumps(gist),
            )
            return response.json()['id']

    def gist_list(self) -> List[str]:
        """Get list of Gists for current user.

        Returns
        -----------
        List of string representations for each gist
        """
        url = '{0}/gists'.format(GITHUB_API)
        response = requests.get(url, headers=self.api_headers)
        gists: List[Dict[str, Any]] = response.json()  # type: ignore
        return [
            gist_utils.format_gist(num, gist) for num, gist in enumerate(gists)
        ]

    def gist_update(
        self,
        gist_id: str,
        filename: str,
    ) -> str:
        """Update Gist from file.

        Parameters
        -----------
        gist_id
            ID of updated gist
        filename
            Name of file with content for Gist

        Returns
        -------
        ID of new gist
        """
        with open(filename, 'r') as gist_file:
            gist = {
                'description': '',
                'public': True,
                'files': {
                    filename: {
                        'content': gist_file.read(),
                    },
                },
            }
            url = '{0}/gists/{1}'.format(GITHUB_API, gist_id)
            response = requests.post(
                url,
                headers=self.api_headers,
                data=json.dumps(gist),
            )
            return response.json()['id']

    def gist_download(
        self,
        gist_id: str,
        filename: str,
    ) -> None:
        """Dowload gist and store it on given path.

        Parameters
        -----------
        gist_id
            ID of gist
        filename
            Path to store the gist.
        """
        with open(filename, 'w') as gist_file:
            url = '{0}/gists/{1}'.format(GITHUB_API, gist_id)
            response = requests.get(url, headers=self.api_headers)
            gist_files: Dict[str, Any] = response.json()[  # type: ignore
                'files'
            ]
            gist_name = list(gist_files.keys())[0]
            gist_file.write(gist_files[gist_name]['content'])

    def gist_delete(self, gist_id: str) -> None:
        """Delete given Gist.

        Parameters
        -----------
        gist_id
            ID of gist
        """
        url = '{0}/gists/{1}'.format(GITHUB_API, gist_id)
        requests.delete(url, headers=self.api_headers)
