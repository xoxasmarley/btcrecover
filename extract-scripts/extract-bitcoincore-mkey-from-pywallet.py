#!/usr/bin/python

# extract-bitcoincore-mkey.py -- Bitcoin wallet master key extractor
# Copyright (C) 2014 Christopher Gurnee
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License version 2 for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

# If you find this program helpful, please consider a small donation
# donation to the developer at the following Bitcoin address:
#
#           17LGpN2z62zp7RS825jXwYtE7zZ19Mxxu8
#
#                      Thank You!

from __future__ import print_function
import sys, os.path, json, struct, base64, zlib

prog = os.path.basename(sys.argv[0])

if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
    print("usage:", prog, "PYWALLET_DUMPWALLET_FILE", file=sys.stderr)
    sys.exit(2)

wallet_filename = sys.argv[1]

with open(wallet_filename, "rb") as wallet_file:

    # pywallet dump files are largish json files often preceded by a bunch of error messages;
    # search through the file in 16k blocks looking for a particular string which occurs twice
    # inside the mkey object we need (because it appears twice, we're guaranteed one copy
    # will appear whole in at least one block even if the other is split across blocks).
    #
    # For the first block, give up if this doesn't look like a text file
    last_block = ""
    cur_block  = wallet_file.read(16384)
    if sum(1 for c in cur_block if ord(c)>126 or ord(c)==0) > 512: # about 3%
        raise ValueError("Unrecognized pywallet format (does not look like ASCII text)")
    while cur_block:
        found_at = cur_block.find('"nDerivation')
        if found_at >= 0: break
        last_block = cur_block
        cur_block  = wallet_file.read(16384)
    else:
        raise ValueError("Unrecognized pywallet format (can't find mkey)")

    # The mkey data we need should be somewhere in here
    cur_block = last_block + cur_block + wallet_file.read(4096)

# Search backwards for the beginning of the mkey object we need, and decode it
found_at  = cur_block.rfind("{", 0, found_at + len(last_block))
if found_at < 0:
    raise ValueError("Unrecognized pywallet format (can't find mkey opening brace)")
wallet = json.JSONDecoder().raw_decode(cur_block[found_at:])[0]

# Do some sanity checking
#
if not all(name in wallet for name in ("nDerivationIterations", "nDerivationMethod", "nID", "salt")):
    raise ValueError("Unrecognized pywallet format (can't find all mkey attributes)")
#
if wallet["nID"] != 1:
    raise NotImplementedError("Unsupported Bitcoin Core wallet ID " + str(wallet["nID"]))
if wallet["nDerivationMethod"] != 0:
    raise NotImplementedError("Unsupported Bitcoin Core key derivation method " + str(wallet["nDerivationMethod"]))

if "encrypted_key" in wallet:
    encrypted_master_key = wallet["encrypted_key"]
elif "crypted_key" in wallet:
    encrypted_master_key = wallet["crypted_key"]
else:
    raise ValueError("Unrecognized pywallet format (can't find [en]crypted_key attribute)")

encrypted_master_key = base64.b16decode(encrypted_master_key, True)  # True means allow lowercase
salt                 = base64.b16decode(wallet["salt"], True)
iter_count           = int(wallet["nDerivationIterations"])

if len(encrypted_master_key) != 48: raise NotImplementedError("Unsupported encrypted master key length")
if len(salt)                 != 8:  raise NotImplementedError("Unsupported salt length")
if iter_count                <= 0:  raise NotImplementedError("Unsupported iteration count")

print("Bitcoin Core encrypted master key, salt, iter_count, and crc in base64:", file=sys.stderr)

bytes = b"bc:" + encrypted_master_key + salt + struct.pack("<I", iter_count)
crc_bytes = struct.pack("<I", zlib.crc32(bytes) & 0xffffffff)

print(base64.b64encode(bytes + crc_bytes))
