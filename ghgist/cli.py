import argparse
import json

from ghgist import commands


def create_parser() -> argparse.ArgumentParser:  # noqa: 210
    parser = argparse.ArgumentParser(prog='ghgist')
    subparsers = parser.add_subparsers(title='Actions', dest='command')
    subparsers.required = True

    parser_create = subparsers.add_parser(
        'create', help='Create gist from file',
    )
    parser_create.add_argument('filename', type=str)

    subparsers.add_parser(
        'list', help="Display list of current user's gists",
    )

    parse_update = subparsers.add_parser('update', help='Update given gist')
    parse_update.add_argument('gist_id', type=str, help='ID of GitHub Gist')
    parse_update.add_argument(
        'filename',
        type=str,
        help='Name of file for new gist',
    )

    parse_download = subparsers.add_parser(
        'download',
        help='Download given gist',
    )
    parse_download.add_argument('gist_id', type=str, help='ID of GitHub Gist')
    parse_download.add_argument(
        'destination_path', type=str, help='Path to store gist content',
    )

    parse_delete = subparsers.add_parser('delete', help='delete given gist')
    parse_delete.add_argument('gist_id', type=str, help='ID of GitHub Gist')
    return parser


def main() -> None:  # noqa: 210
    """Parse user's input and execute given command."""
    try:
        with open('.ghgist', 'r') as ghgist_file:
            token = json.load(ghgist_file)['ghgist']['settings']['token']
    except KeyError:
        print('Please store Github access token in correct format')  # noqa: 421
        return

    cmd = commands.Commands({
        'Authorization': 'token {0}'.format(token),
        'Accept': 'Accept: application/vnd.github.v3+json',
    })
    cmd_functions = {
        'create': lambda args: cmd.gist_create(args.filename),
        'list': lambda args: print('\n'.join(cmd.gist_list())),  # noqa: 421
        'update': lambda args: cmd.gist_update(args.gist_id, args.filename),
        'download': lambda args: cmd.gist_download(
            args.gist_id, args.destination_path,
        ),
        'delete': lambda args: cmd.gist_delete(args.gist_id),
    }
    args = create_parser().parse_args()
    cmd_function = cmd_functions.get(args.command)
    if cmd_function is not None:
        cmd_function(args)  # type: ignore
    else:
        print('Unknown command')  # noqa: 421


if __name__ == '__main__':
    main()
