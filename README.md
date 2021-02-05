xmpp-omemo-downloader
=====================

A script that downloads and decrypts [OMEMO-encrypted files sent over XMPP][1].
Useful when your XMPP client supports OMEMO-encrypted messages, but not files.

[1]: https://xmpp.org/extensions/inbox/omemo-media-sharing.html

Usage
-----

Run `./xmpp-omemo-downloader.py` for usage information.

Dependencies
------------

* Python ≥ 3.7
* Python package: [requests]
* Python package: [pycryptodome]

Run `pip3 install -r requirements.txt` to install the Python packages. You can
also use `requirements.freeze.txt` instead to install specific versions of the
dependencies that have been verified to work.

[pycryptodome]: https://pypi.org/project/pycryptodome
[requests]: https://pypi.org/project/requests

License
-------

xmpp-omemo-downloader is licensed under version 3 or later of the GNU Affero
General Public License. See [LICENSE](LICENSE).
