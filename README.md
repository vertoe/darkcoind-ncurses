darkcoind-ncurses v0.0.22
=========================

ncurses front-end for darkcoind

![ScreenShot](/screenshots/bitcoind-ncurses-splash.png)
![ScreenShot](/screenshots/bitcoind-ncurses-monitor.png)
![ScreenShot](/screenshots/bitcoind-ncurses-block.png)
![ScreenShot](/screenshots/bitcoind-ncurses-tx.png)
![ScreenShot](/screenshots/bitcoind-ncurses-peers.png)
![ScreenShot](/screenshots/bitcoind-ncurses-wallet.png)
![ScreenShot](/screenshots/bitcoind-ncurses-net.png)
![ScreenShot](/screenshots/bitcoind-ncurses-forks.png)
![ScreenShot](/screenshots/bitcoind-ncurses-console.png)

produced by Amphibian (azeteki, Atelopus_zeteki)

dependencies
------------

* tested with python 2.7.3, darkcoind 0.10.17.24
* jgarzik's bitcoinrpc library port for darkcoin (https://github.com/vertoe/python-darkcoinrpc)
* (Windows only) python ncurses library (http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses)

features
--------

* updating ticker showing darkcoind's status (via RPC)
* view arbitrary block contents quickly
* facility to view transactions in current block and trace back through their inputs (with -txindex)
* view transactions from your wallet - txid, amounts, cumulative balance
* view connected peers
* basic debug console functionality (only for testnet use at present)

usage
-----

copy your darkcoin.conf to darkcoind-ncurses's folder

alternatively, create a file with the following details:
```
rpcuser=xxx
rpcpassword=yyy
testnet=0
```

this is an early development release. expect (safe) breakage

launch
------

replace 'python' with 'python2' if you also have python3 installed.
```
$ python main.py
$ python main.py -c some_other_config_file.conf
```

todo
----

* ensure terminal always returns to sane state on program exit
* mean block size/tx count over last X blocks
* transaction creation support (if I feel suicidal)
* more testing for edge cases (paramount for above)

frog food
---------

found darkcoind-ncurses useful? donations are your way of showing that!

my main machine is currently a 6 year old Atom laptop. upgrading that would be rather useful. cheers!

![ScreenShot](/screenshots/donation-qr.png)

**1FrogqMmKWtp1AQSyHNbPUm53NnoGBHaBo**
