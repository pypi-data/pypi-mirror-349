# HTTP server for Atom feed of TLS certificate expirations
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

from asyncio import start_server
from base64 import urlsafe_b64encode as base64
from datetime import datetime
from functools import partial
from urllib.parse import parse_qs, urljoin, urlsplit
from xml.etree.ElementTree import (Element as xml_element,
                                   SubElement as xml_subelement,
                                   indent, tostring as xml_to_string)

from . import __version__

__all__ = ['listen']


def path(hostname, port, issuer, serial):
    """Return the relative URL for the given certificate's details."""
    issuer_b64 = base64(issuer.encode()).decode()
    return f'{hostname}/{port}/{issuer_b64}/{serial}'


def body(not_before, not_after, hostname, port, serial, issuer):
    """Describe the given certificate in XHTML."""
    return (('h1', 'TLS certificate information'),
            ('dl',
             ('dt', 'Domain'), ('dd', hostname),
             ('dt', 'Port'), ('dd', port),
             ('dt', 'Issuer'), ('dd', issuer),
             ('dt', 'Serial number'), ('dd', serial),
             ('dt', 'Valid from'), ('dd', not_before),
             ('dt', 'Valid until'), ('dd', not_after)))


def entry(base_url, cert):
    """Construct Atom entry for the given TLS certificate."""
    not_before, not_after, hostname, port, serial, issuer = cert
    url = urljoin(base_url, path(hostname, port, issuer, serial))
    return ('entry',
            ('author', ('name', issuer)),
            ('content', {'type': 'xhtml'},
             ('div', {'xmlns': 'http://www.w3.org/1999/xhtml'}, *body(*cert))),
            ('id', url),
            ('link', {'rel': 'alternate', 'type': 'text/plain', 'href': url}),
            ('title', (f'TLS cert for {hostname} will expire at {not_after}')),
            ('updated', not_before))


def xml(tree, parent=None):
    """Construct XML element from the given tree."""
    tag, attrs, children = ((tree[0], tree[1], tree[2:])
                            if isinstance(tree[1], dict)
                            else (tree[0], {}, tree[1:]))
    if parent is None:
        elem = xml_element(tag, attrs)
    else:
        elem = xml_subelement(parent, tag, attrs)
    for child in children:
        if isinstance(child, str):
            elem.text = child
        else:
            xml(child, elem)
    if parent is None:
        indent(elem)
    return elem


async def handle(certs, base_url, reader, writer):
    """Handle HTTP request."""
    summaries = tuple(cert.rstrip().split(maxsplit=5)
                      for cert in certs.read_text().splitlines())
    lookup = {f'/{path(hostname, port, issuer, serial)}':
              (not_before, not_after, hostname, port, serial, issuer)
              for not_before, not_after, hostname, port, serial, issuer
              in summaries}
    request = await reader.readuntil(b'\r\n')
    url = request.removeprefix(b'GET ').rsplit(b' HTTP/', 1)[0]
    url_parts = urlsplit(url.decode())
    domains = tuple(parse_qs(url_parts.query).get('domain', ['']))

    if not request.startswith(b'GET '):
        writer.write(b'HTTP/1.1 405 Method Not Allowed\r\n')
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return
    elif url_parts.path == '/':  # Atom feed
        writer.write(b'HTTP/1.1 200 OK\r\n')
        writer.write(b'Content-Type: application/atom+xml\r\n')
        feed = xml(('feed', {'xmlns': 'http://www.w3.org/2005/Atom'},
                    ('id', base_url),
                    ('link', {'rel': 'self', 'href': base_url}),
                    ('title', certs.name),
                    ('updated', datetime.now().isoformat()),
                    ('generator', {'uri': 'https://trong.loang.net/scadere/about',
                                   'version': __version__},
                     'Scadere'),
                    *(entry(base_url, cert)
                      for cert in summaries if cert[2].endswith(domains))))
        content = xml_to_string(feed, 'unicode', xml_declaration=True,
                                default_namespace=None).encode()
        writer.write(f'Content-Length: {len(content)}\r\n\r\n'.encode())
        writer.write(content)
    elif url_parts.path in lookup:  # accessible Atom entry's link/ID
        writer.write(b'HTTP/1.1 200 OK\r\n')
        writer.write(b'Content-Type: application/xhtml+xml\r\n')
        (not_before, not_after,
         hostname, port, serial, issuer) = lookup[url_parts.path]
        page = xml(('html', {'xmlns': 'http://www.w3.org/1999/xhtml',
                             'lang': 'en'},
                    ('head',
                     ('meta', {'name': 'color-scheme',
                               'content': 'dark light'}),
                     ('meta', {'name': 'viewport',
                               'content': ('width=device-width,'
                                           'initial-scale=1.0')}),
                     ('link', {'rel': 'icon', 'href': 'data:,'}),
                     ('title', f'TLS certificate - {hostname}:{port}')),
                    ('body', *body(not_before, not_after,
                                   hostname, port, serial, issuer))))
        content = xml_to_string(page, 'unicode', xml_declaration=True,
                                default_namespace=None).encode()
        writer.write(f'Content-Length: {len(content)}\r\n\r\n'.encode())
        writer.write(content)
    else:
        writer.write(b'HTTP/1.1 404 Not Found\r\n')
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def listen(certs, base_url, host, port):
    """Serve HTTP server for TLS certificate expirations' Atom feed."""
    server = await start_server(partial(handle, certs, base_url), host, port)
    async with server:
        print('Serving on', end=' ')
        print(*(socket.getsockname() for socket in server.sockets), sep=', ')
        await server.serve_forever()
