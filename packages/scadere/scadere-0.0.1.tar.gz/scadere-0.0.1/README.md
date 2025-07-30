# Scadere

Scadere is a TLS certificate renewal remider.  It checks for certificates
that are about to expire and provides an Atom feed for notification.

## Usage

### Expiration checking

```console
$ scadere check --help
Usage: scadere check [-h] [-d DAYS] [-o PATH] HOST[:PORT] [HOST[:PORT] ...]

Check TLS certificate expiration of HOST, where PORT defaults to 443.

Options:
  -h, --help            show this help message and exit
  -d DAYS, --days=DAYS  days before expiration (default to 7)
  -o PATH, --output=PATH
                        output file (default to stdout)
```

It is recommended to run `scadere check` as a cron job.

### Expiration notification

```console
$ scadere listen --help
Usage: scadere listen [-h] INPUT URL [[HOST][:PORT]]

Serve the TLS certificate expiration feed from INPUT file
for base URL at HOST:PORT, where HOST defaults to localhost
and PORT is selected randomly if not specified.

Options:
  -h, --help  show this help message and exit
```

## Contributing

Patches should be sent to [chung@loa.loang.net][loang mailing list]
using [`git send-email`][git send-email], with the following configuration:

    git config sendemail.to 'chung@loa.loang.net'
    git config format.subjectPrefix 'PATCH scadere'

## Copying

![AGPLv3](https://www.gnu.org/graphics/agplv3-155x51.png)

Scadere is free software: you can redistribute it and/or modify it
under the terms of the GNU [Affero General Public License][agplv3] as
published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

[loang mailing list]: https://loa.loang.net/chung
[git send-email]: https://git-send-email.io
[agplv3]: https://www.gnu.org/licenses/agpl-3.0.html
