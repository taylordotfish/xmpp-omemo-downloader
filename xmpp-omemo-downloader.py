#!/usr/bin/env python3
# Copyright (C) 2020 taylor.fish <contact@taylor.fish>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from Crypto.Cipher import AES
from requests.exceptions import RequestException
import requests

import binascii
import os
import re
import sys

USAGE = """\
usage: xmpp-omemo-downloader.py <aesgcm-url>

<aesgcm-url> should be a URL that begins with “aesgcm://”. You must also
include all of the text after the hash character (#) in the URL.
"""

if len(sys.argv) != 2:
    print(USAGE, end="", file=sys.stderr)
    sys.exit(1)

if sys.argv[1] in ["-h", "--help"]:
    print(USAGE, end="")
    sys.exit()

url = sys.argv[1].strip()
match = re.fullmatch(r"aesgcm://([^#]+)#([0-9A-Fa-f]+)", url)
if not match:
    print("error: invalid URL", file=sys.stderr)
    sys.exit(1)

base_url, params = match.groups()
http_url = f"https://{base_url}"
filename = re.search(r"([^/]+)$", base_url).group(1)
params_dec = binascii.unhexlify(params)
iv, key = params_dec[:12], params_dec[12:]
aes = AES.new(key, AES.MODE_GCM, nonce=iv)

print(f"downloading {http_url}", file=sys.stderr)
try:
    resp = requests.get(http_url)
except RequestException:
    print("error: got exception while downloading file:", file=sys.stderr)
    raise

if resp.status_code != 200:
    print(f"error: bad HTTP status ({resp.status})", file=sys.stderr)
    sys.exit(1)

enc = resp.content[:-16]  # remove OMEMO auth tag
dec = aes.decrypt(enc)


def names():
    yield filename
    i = 1
    while True:
        yield f"{filename}.{i}"
        i += 1


for local_name in names():
    try:
        fd = os.open(local_name, os.O_CREAT | os.O_EXCL, 0o666)
    except FileExistsError:
        continue
    os.close(fd)
    break

with open(local_name, "wb") as f:
    f.write(dec)
print(f"saved file to {local_name}")
