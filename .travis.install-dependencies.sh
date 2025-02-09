#!/bin/bash

# Best practice for Travis CI is to use Python virtualenv instead of the system Python.
# Unfortunately, the virtualenv which Travis CI sets up has a broken bsddb module,
# doesn't have PyCrypto preinstalled, and doesn't play nice with dependencies from
# the Armory .deb distribution, so we just use the system Python instead.

set -e

# Download and install latest stable Armory plus prerequisites

DOWNLOADS="`curl -fsS --retry 10 https://s3.amazonaws.com/bitcoinarmory-media/announce.txt | awk '/^downloads/{print $2}'`"
echo "$DOWNLOADS" | grep -q '^https://' || { echo "Can't find Armory downloads URL"; exit 1; }

LATEST="`curl -fsS --retry 10 \"$DOWNLOADS\" | grep '^Armory [0-9.]* Ubuntu [0-9.,]*12\.04[0-9.,]* 64 ' | sort -k 2V | tail -1 | awk '{print $6}'`"
echo "$LATEST" | grep -q '^https://' || { echo "Can't find latest Armory download URL"; exit 1; }

curl -fsS --retry 10 -o 'armory.deb' "$LATEST"

sudo apt-get -q update
sudo apt-get -yq install gdebi-core
sudo gdebi -nq armory.deb
