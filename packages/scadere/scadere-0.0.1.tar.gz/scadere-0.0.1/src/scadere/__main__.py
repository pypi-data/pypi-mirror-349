# Executable entry point
# Copyright (C) 2025  Nguyễn Gia Phong
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from argparse import ArgumentParser, FileType, HelpFormatter
from asyncio import run
from datetime import datetime, timedelta, timezone
from pathlib import Path
from sys import stdout

from . import __version__
from .check import check
from .listen import listen


class GNUHelpFormatter(HelpFormatter):
    """Help formatter for ArgumentParser following GNU Coding Standards."""

    def add_usage(self, usage, actions, groups, prefix='Usage: '):
        """Substitute 'Usage:' for 'usage:'."""
        super().add_usage(usage, actions, groups, prefix)

    def start_section(self, heading):
        """Substitute 'Options:' for 'options:'."""
        super().start_section(heading.capitalize())

    def _format_action_invocation(self, action):
        """Format --long-option=argument."""
        if not action.option_strings or action.nargs is not None:
            return super()._format_action_invocation(action)
        arg = self._format_args(action,
                                self._get_default_metavar_for_optional(action))
        return ', '.join(f"{opt}{'=' if opt.startswith('--') else ' '}{arg}"
                         for opt in action.option_strings)

    def add_argument(self, action):
        """Suppress positional arguments."""
        if action.option_strings:
            super().add_argument(action)


class NetLoc:
    def __init__(self, default_port):
        self.default_port = default_port

    def __call__(self, string):
        """Return hostname and port from given netloc."""
        if ':' not in string:
            return string, self.default_port
        hostname, port = string.rsplit(':', 1)
        return hostname, int(port)  # ValueError to be handled by argparse


def main():
    """Parse arguments and launch subprogram."""
    parser = ArgumentParser(prog='scadere', allow_abbrev=False,
                            formatter_class=GNUHelpFormatter)
    parser.add_argument('-v', '--version', action='version',
                        version=f'%(prog)s {__version__}')
    subparsers = parser.add_subparsers(help='subcommand help', required=True)

    check_description = ('Check TLS certificate expiration of HOST,'
                         ' where PORT defaults to 443.')
    check_parser = subparsers.add_parser('check',
                                         description=check_description,
                                         formatter_class=GNUHelpFormatter)
    check_parser.set_defaults(subcommand='check')
    check_parser.add_argument('netloc', metavar='HOST[:PORT]',
                              nargs='+', type=NetLoc(443))
    check_parser.add_argument('-d', '--days', type=float, default=7,
                              help='days before expiration (default to 7)')
    check_parser.add_argument('-o', '--output', metavar='PATH',
                              type=FileType('w'), default=stdout,
                              help='output file (default to stdout)')

    listen_description = ('Serve the TLS certificate expiration feed'
                          ' from INPUT file for base URL at HOST:PORT,'
                          ' where HOST defaults to localhost and PORT'
                          ' is selected randomly if not specified.')
    listen_parser = subparsers.add_parser('listen',
                                          description=listen_description,
                                          formatter_class=GNUHelpFormatter)
    listen_parser.add_argument('certs', metavar='INPUT', type=Path)
    listen_parser.add_argument('base_url', metavar='URL')
    listen_parser.add_argument('netloc', metavar='[HOST][:PORT]', nargs='?',
                               type=NetLoc(None), default=('localhost', None))
    listen_parser.set_defaults(subcommand='listen')

    args = parser.parse_args()
    if args.subcommand == 'check':
        with args.output:
            after = datetime.now(tz=timezone.utc) + timedelta(days=args.days)
            check(args.netloc, after, args.output)
    elif args.subcommand == 'listen':
        run(listen(args.certs, args.base_url, *args.netloc))


if __name__ == '__main__':
    main()
