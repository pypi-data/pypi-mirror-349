# TLS certificate expiration checker
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

from email.utils import parsedate_to_datetime as parsedate
from itertools import chain
from socket import AF_INET, socket
from ssl import create_default_context as tls_context
from sys import stderr

__all__ = ['check']


def check(netlocs, after, output):
    """Check if each netloc's TLS certificate expires after given time.

    Print the certificate's summary to output file if that is the case.
    """
    ctx = tls_context()
    for hostname, port in netlocs:
        netloc = f'{hostname}:{port}'
        stderr.write(f'TLS certificate for {netloc} ')
        try:
            with ctx.wrap_socket(socket(AF_INET),
                                 server_hostname=hostname) as conn:
                conn.connect((hostname, port))
                cert = conn.getpeercert()
        except Exception as e:
            stderr.write(f'cannot be retrieved: {e}\n')
        else:
            ca = dict(chain.from_iterable(cert['issuer']))['organizationName']
            not_before = parsedate(cert['notBefore'])
            not_after = parsedate(cert['notAfter'])
            if after < not_after:
                after_seconds = after.isoformat(timespec='seconds')
                stderr.write(f'will not expire at {after_seconds}\n')
            else:
                stderr.write(f'will expire at {not_after.isoformat()}\n')
                print(not_before.isoformat(), not_after.isoformat(),
                      # As unique identifier
                      hostname, port, cert['serialNumber'], ca,
                      file=output)
