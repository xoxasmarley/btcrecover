# *btcrecover* #

## extract scripts ##

Sometimes, it is not desirable to run *btcrecover* directly on the computer which stores the target wallet file. For example:

 * A computer or a cloud-based virtual machine with faster CPUs or GPUs might be a better place to run *btcrecover*.
 * Configuring *btcrecover* to search for your password correctly can be tricky; you might be interested in finding someone who can configure and run *btcrecover* for you on their computer.
 * You may not trust that *btcrecover* is free from harmful bugs or other malicious behavior. *btcrecover* is open source, and requires no untrustworthy binaries be installed. However it's also a fairly long and complicated Python script, which makes it difficult even for other Python programmers to be certain that it doesn't contain any harmful code (either intentionally malicious or just by accident).

The extract scripts in this directory are relatively short and simple scripts which extract the just enough information from a wallet file to allow *btcrecover* to perform a password search. With the exception of Armory, these scripts never extract enough information to put any of your bitcoin funds at risk, even after the password is found. For Armory, only a single (typically unused) address and private key are extracted, putting only that one address at risk.

For more information regarding *btcrecover*, please see [TUTORIAL.md](../TUTORIAL.md).

### Download ###

You can download the entire *btcrecover* package from: <https://github.com/gurnec/btcrecover/archive/master.zip>

If you'd prefer to download just a single extract script, please select the one for your wallet software from below, then right click and choose “Save link as...” or “Save target as...”:

 * Armory - <https://github.com/gurnec/btcrecover/raw/master/extract-scripts/extract-armory-privkey.py>
 * Bitcoin Core - <https://github.com/gurnec/btcrecover/raw/master/extract-scripts/extract-bitcoincore-mkey.py>
 * Blockchain main password - <https://github.com/gurnec/btcrecover/raw/master/extract-scripts/extract-blockchain-main-data.py>
 * Blockchain second password -  <https://github.com/gurnec/btcrecover/raw/master/extract-scripts/extract-blockchain-second-hash.py>
 * Electrum - <https://github.com/gurnec/btcrecover/raw/master/extract-scripts/extract-electrum-halfseed.py>
 * MultiBit - <https://github.com/gurnec/btcrecover/raw/master/extract-scripts/extract-multibit-privkey.py>

If you're on Windows, you will also need to install the latest version of Python 2.7. For Armory wallets, you must install the 32-bit version. For any other wallets, you may install either the 32-bit or the 64-bit version. Currently this is the “Python 2.7.6 Windows Installer” for the 32-bit version, or the “Python 2.7.6 Windows X86-64 Installer” for the 64-bit version, both available here: <https://www.python.org/download/>. For Armory wallets, you must also have Armory v0.91 or later installed.


### Usage for Armory ###

Open Armory (in offline mode if you like), and take note of the wallet ID whose password you've lost. Open this wallet, and click Receive Bitcoins to display a new Bitcoin address. Add a label to the address, such as "Recovery address - DO NOT USE", and copy the Bitcoin address to someplace temporary (a Notepad document, a Post-It, or wherever). Quit Armory.

If you've ever used this wallet on more than one computer, the address you just created might already exist. It's up to you to find an unused and unpublished address for this procedure, and to never use this address in the future. You can check if the address has been used in the past at <https://blockchain.info/>, but you're the only one who might know if you've given this address out to someone else before today.

After downloading the script, **make a copy of your wallet file into a different folder** (to make it easy, into the same folder as the extract script). As an example for Windows, click on the Start Menu, then click “Run...”, and then type this to open your Armory folder which contains your wallet files: `%appdata%\Armory`. From here you can copy and paste the wallet file that matches the wallet ID you noted earlier into a separate folder. Next you'll need to open a Command Prompt window and type something like this (depending on where the downloaded script is, and assuming you've made a copy of your wallet file into the same folder):

    cd \Users\Chris\Downloads\btcrecover-master\extract-scripts
    C:\python27\python extract-armory-privkey.py armory_2dRkxw76K_.wallet extract 1LhkzLtY5drbUxXvsk8LmU1aRFz13EDcp4

Of course, you need to replace the wallet file name with yours, and the Bitcoin address with the one you created earlier. You should get a message which looks like this as a result. You should double-check that the address matches the one you just created (along with the label which you gave to it):

    1LhkzLtY5drbUxXvsk8LmU1aRFz13EDcp4 First:04/19/14 Last:04/19/14 Recovery address - DO NOT USE

    WARNING: once decrypted, this will provide access to all Bitcoin
             funds available now and in the future of this one address

    Armory address, encrypted private key, iv, kdf parameters, and crc in base64:
    YXI62B+/jb1Pthvjsrh+LlW5PS87FpfdBR3d5G1yWPY0cEUl3D+U2382qq0YkqoBDfnHDda/a3bOay/OKq9UWy/nra5SGyMAAEAAAgAAABiymPHbLR+L8tKm+wpnzDioxV+lMgAwB2SH0hpYvez8w5aWGQ==

When you (or someone else) runs *btcrecover* to search for passwords, you will not need your wallet file, only the output from *extract-armory-privkey.py*. To continue the example:

    cd \Users\Chris\Downloads\btcrecover-master
    C:\python27\python btcrecover.py --extract-data --tokenlist tokens.txt
    Please enter the data from the extract script
    > YXI62B+/jb1Pthvjsrh+LlW5PS87FpfdBR3d5G1yWPY0cEUl3D+U2382qq0YkqoBDfnHDda/a3bOay/OKq9UWy/nra5SGyMAAEAAAgAAABiymPHbLR+L8tKm+wpnzDioxV+lMgAwB2SH0hpYvez8w5aWGQ==
    WARNING: an Armory private key, once decrypted, provides access to that key's Bitcoin
    ...
    Password found: xxxx

#### Armory Technical Details ####

The *extract-armory-privkey.py* script is intentionally short and should be easy to read for any Python programmer. As detailed above, it extracts a single address and private key using the official armoryengine library, putting this one address at risk. However, without access to the rest of your wallet file, the rest of your addresses and private keys are not at risk, even after a successful password guess and decryption.

Armory automatically pre-generates 100 addresses and private keys before they are needed, which is why you can ask it to display a "new" address without a password. If you've asked for and then used 100 new addresses without providing a password, it's possible that Armory will be unable to provide a new address (without a password) as required by this procedure. If this is the case, you'll have no choice but to choose an already used address. To assist in choosing such an address, you can run `extract-armory-privkey.py list` from the command line to display a list of addresses available in the wallet which include an encrypted private key (including pre-generated addresses that may not be visible via the Armory GUI) along with the first and last known dates of use for each address. These dates of known use do not check the current block chain; you should always check a questionable address on <https://blockchain.info/> to check it's current balance before you use it with this procedure.


### Usage for Bitcoin Core ###

After downloading the script, **make a copy of your wallet.dat file into a different folder** (to make it easy, into the same folder as *extract-bitcoincore-mkey.py*). As an example for Windows, click on the Start Menu, then click “Run...”, and then type this to open your Bitcoin folder which contains your wallet.dat file: `%appdata%\Bitcoin`. From here you can copy and paste your wallet.dat file into a separate folder. Next you'll need to open a Command Prompt window and type something like this (depending on where the downloaded script is, and assuming you've made a copy of your wallet.dat into the same folder):

    cd \Users\Chris\Downloads\btcrecover-master\extract-scripts
    C:\python27\python extract-bitcoincore-mkey.py wallet.dat

You should get a message which looks like this as a result:

    Bitcoin Core encrypted master key, salt, iter_count, and crc in base64:
    lV/wGO5oAUM42KTfq5s3egX3Uhk6gc5gEf1R3TppgzWNW7NGZQF5t5U3Ik0qYs5/dprb+ifLDHuGNQIA+8oRWA==

When you (or someone else) runs *btcrecover* to search for passwords, you will not need your wallet file, only the output from *extract-bitcoincore-mkey.py*. To continue the example:

    cd \Users\Chris\Downloads\btcrecover-master
    C:\python27\python btcrecover.py --extract-data --tokenlist tokens.txt
    Please enter the data from the extract script
    > lV/wGO5oAUM42KTfq5s3egX3Uhk6gc5gEf1R3TppgzWNW7NGZQF5t5U3Ik0qYs5/dprb+ifLDHuGNQIA+8oRWA==
    ...
    Password found: xxxx

#### Bitcoin Core Technical Details ####

The *extract-bitcoincore-mkey.py* script is intentionally short and should be easy to read for any Python programmer. It opens a wallet.dat file using the Python bsddb.db library (the Berkeley DB library which comes with Python 2.7), and then extracts a single key/value pair with the key string of `\x04mkey\x01\x00\x00\x00`. This key/value pair contains an encrypted version of the Bitcoin Core “master key”, or mkey for short, along with some other information required to try decrypting the mkey, specifically the mkey salt and iteration count. This information is then converted to base64 format for easy copy/paste, and printed to the screen.

The encrypted mkey is useful to *btcrecover*, but it does not contain any of your Bitcoin address or private key information. *btcrecover* can attempt to decrypt the mkey by trying different password combinations. Should it succeed, it and whoever runs it will then know the password to your wallet file, but without the rest of your wallet file, the password and the decrypted mkey are of no use.


### Usage for Blockchain ###

Locate your Blockchain wallet backup file (it's usually named `wallet.aes.json`), and **make a copy of it into a different folder** (to make it easy, into the same folder as the extract script). Next you'll need to open a Command Prompt window and type something like this (depending on where the downloaded script is, and assuming you've made a copy of your wallet file into the same folder):

    cd \Users\Chris\Downloads\btcrecover-master\extract-scripts
    C:\python27\python extract-blockchain-main-data.py wallet.aes.json

Of course, you need to replace the wallet file name with yours. You should get a message which looks like this as a result:

    Blockchain first 16 encrypted bytes, iv, and iter_count in base64:
    Yms6abF6aZYdu5sKpStKA4ihra6GEAeZTumFiIM0YQUkTjcQJwAAj8ekAQ==

When you (or someone else) runs *btcrecover* to search for passwords, you will not need your wallet file, only the output from *extract-blockchain-main-data.py*. To continue the example:

    cd \Users\Chris\Downloads\btcrecover-master
    C:\python27\python btcrecover.py --extract-data --tokenlist tokens.txt
    Please enter the data from the extract script
    > Yms6abF6aZYdu5sKpStKA4ihra6GEAeZTumFiIM0YQUkTjcQJwAAj8ekAQ==
    ...
    Password found: xxxx

#### Blockchain Second Passwords ####

If you've enabled the Second Password (also called the double encryption) feature of your Blockchain wallet, and if you need to search for this second password, you must start by finding the main password if you don't already have it (see above). Once you have your main password, take your wallet backup file (it's usually named `wallet.aes.json`), and **make a copy of it into a different folder** (to make it easy, into the same folder as the extract script). Next you'll need to open a Command Prompt window and type something like this (depending on where the downloaded script is, and assuming you've made a copy of your wallet file into the same folder):

    cd \Users\Chris\Downloads\btcrecover-master\extract-scripts
    C:\python27\python extract-blockchain-second-hash.py wallet.aes.json
    Please enter the Blockchain wallet's main password:

You need to enter your wallet's main password when prompted so that the extract script can remove the first level of encryption to gain access to the second level of encrypted data. You should get a message which looks like this as a result:

    Blockchain second password hash, salt, and iter_count in base64:
    YnM6LeP7peG853HnQlaGswlwpwtqXKwa/1rLyeGzvKNl9HpyjnaeTCZDAaC4LbJcVkxaECcAACwXY6w=

When you (or someone else) runs *btcrecover* to search for passwords, you will not need your wallet file, only the output from *extract-blockchain-second-hash.py*. To continue the example:

    cd \Users\Chris\Downloads\btcrecover-master
    C:\python27\python btcrecover.py --extract-data --tokenlist tokens.txt
    Please enter the data from the extract script
    > YnM6LeP7peG853HnQlaGswlwpwtqXKwa/1rLyeGzvKNl9HpyjnaeTCZDAaC4LbJcVkxaECcAACwXY6w=
    ...
    Password found: xxxx

Please note that you must either download the entire *btcrecover* package which includes an AES decryption library, or you must already have PyCrypto installed in order to use the *extract-blockchain-second-hash.py* script.

#### Blockchain Technical Details ####

The *extract-blockchain-main-data.py* script is intentionally short and should be easy to read for any Python programmer. This script extracts the first 32 bytes of encrypted data from a Blockchain wallet, of which 16 bytes are an AES initialization vector, and the remaining 16 bytes are the first encrypted AES block. This information is then converted to base64 format for easy copy/paste, and printed to the screen. The one encrypted block does not contain any private key information, but once decrypted it does contain a non-sensitive string (specifically the string "guid") which can be used by *btcrecover* to test for a successful password try.

The *extract-blockchain-second-hash.py* script is a bit longer, but it should still be short enough for most Python programmers to read and understand. After decrypting the first level of encryption of a Blockchain wallet, it extracts a password hash and salt which can be used by *btcrecover* to test for a successful password try. It does not extract any of the encrypted private keys.

Without access to the rest of your wallet file, the bits of information extracted by these scripts alone do not put any of your Bitcoin funds at risk, even after a successful password guess and decryption.


### Usage for Electrum ###

After downloading the script, **make a copy of your wallet file into a different folder** (to make it easy, into the same folder as *extract-electrum-halfseed.py*). As an example for Windows, click on the Start Menu, then click “Run...”, and then type this to open the folder which contains the first wallet file created by Electrum after it is installed: `%appdata%\Electrum\wallets`. From here you can copy and paste your wallet file, usually named `default_wallet`, into a separate folder. Next you'll need to open a Command Prompt window and type something like this (depending on where the downloaded script is, and assuming you've made a copy of your wallet file into the same folder):

    cd \Users\Chris\Downloads\btcrecover-master\extract-scripts
    C:\python27\python extract-electrum-halfseed.py default_wallet

Of course, you need to replace the wallet file name with yours. You should get a message which looks like this as a result:

    First half of encrypted Electrum seed, iv, and crc in base64:
    ZWw6kLJxTDF7LxneT7c5DblJ9k9WYwV6YUIUQO+IDiIXzMUZvsCT

When you (or someone else) runs *btcrecover* to search for passwords, you will not need your wallet file, only the output from *extract-electrum-halfseed.py*. To continue the example:

    cd \Users\Chris\Downloads\btcrecover-master
    C:\python27\python btcrecover.py --extract-data --tokenlist tokens.txt
    Please enter the data from the extract script
    > ZWw6kLJxTDF7LxneT7c5DblJ9k9WYwV6YUIUQO+IDiIXzMUZvsCT
    ...
    Password found: xxxx

#### Electrum Technical Details ####

The *extract-electrum-halfseed.py* script is intentionally short and should be easy to read for any Python programmer. An Electrum encrypted seed is 64 bytes long. It contains a 16-byte AES initialization vector, followed by 48 bytes of encrypted seed data, the last 16 of which are padding (so just 32 bytes of actual seed data). The script extracts the 16-byte initialization vector and just the first 16 bytes of actual seed data (50% of the seed).

Because only half of the seed is extracted, the private keys cannot be feasibly reconstructed even after the half-seed is decrypted (assuming the password search succeeds). Because these 16 characters are hex encoded, *btcrecover* can use them alone to check passwords. It tries decrypting the characters with each password, and once the result is a valid 16-character long hex-encoded string, it has found the correct password.

Without access to the rest of your wallet file, it is extremely unlikely that these 16 characters alone could put any of your Bitcoin funds at risk, even after a successful password guess and decryption.


### Usage for MultiBit ###

*btcrecover* doesn’t operate directly on MultiBit wallet files, instead it operates on MultiBit private key backup files. When you first add a password to your MultiBit wallet, and after that each time you add a new receiving address or change your wallet password, MultiBit creates an encrypted private key backup file in a `key-backup` directory that's near the wallet file. These private key backup files are much faster to try passwords against (by a factor of over 1,000), which is why *btcrecover* uses them. For the default wallet that is created when MultiBit is first installed, this directory is located here:

    %appdata%\MultiBit\multibit-data\key-backup

The key files have names which look like `walletname-20140407200743.key`. If you've created additional wallets, their `key-backup` directories will be located elsewhere and it's up to you to locate them.

For more details on locating your MultiBit private key backup files, see: <https://www.multibit.org/en/help/v0.5/help_fileDescriptions.html>

Once you've located the correct MultiBit private key backup file, **make a copy of it into a different folder** (to make it easy, into the same folder as the extract script). As an example for Windows, click on the Start Menu, then click “Run...”, and then type this to open the private key backup folder for the first wallet which MultiBit creates (this might not be the one you want, though...): `%appdata%\MultiBit\multibit-data\key-backup`. From here you can copy and paste a private key backup file into a separate folder. Next you'll need to open a Command Prompt window and type something like this (depending on where the downloaded script is, and assuming you've made a copy of the private key file into the same folder):

    cd \Users\Chris\Downloads\btcrecover-master\extract-scripts
    C:\python27\python extract-multibit-privkey.py multibit-20140407200743.key

Of course, you need to replace the private key file name with yours. You should get a message which looks like this as a result:

    MultiBit partial first encrypted private key, salt, and crc in base64:
    bWI6sTaHldcBFFj9zlgNpO1szOwy8elpl20OWgj+lA==

When you (or someone else) runs *btcrecover* to search for passwords, you will not need your wallet file or the private key file, only the output from *extract-multibit-privkey.py*. To continue the example:

    cd \Users\Chris\Downloads\btcrecover-master
    C:\python27\python btcrecover.py --extract-data --tokenlist tokens.txt
    Please enter the data from the extract script
    > bWI6sTaHldcBFFj9zlgNpO1szOwy8elpl20OWgj+lA==
    ...
    Password found: xxxx

#### MultiBit Technical Details ####

The *extract-multibit-privkey.py* script is intentionally short and should be easy to read for any Python programmer. This script extracts 8 bytes of password salt plus the first 16 encrypted base58-encoded characters (out of 52) from the first private key from a MultiBit private key backup file. Because less than 30% of a single private key is extracted, the private key itself cannot be feasibly reconstructed even after these first 16 characters are decrypted (assuming the password search succeeds). Because these 16 characters are base58 encoded, *btcrecover* can use them alone to check passwords. It tries decrypting the characters with each password, and once the result is a valid 16-character long base58-encoded private key prefix, it has found the correct password.

Without access to the rest of your private key backup file or your wallet file, these 16 characters alone do not put any of your Bitcoin funds at risk, even after a successful password guess and decryption.


### Limitations ###

As mentioned in the [Usage for Armory](#usage-for-armory) section, the address and private key extracted from Armory wallets does put that one address at risk.
