darkcoind-ncurses v0.0.23
=========================

ncurses front-end for darkcoind

![ScreenShot](/screenshots/darkcoind-ncurses-splash.png)
![ScreenShot](/screenshots/bitcoind-ncurses-monitor.png)
![ScreenShot](/screenshots/bitcoind-ncurses-block.png)
![ScreenShot](/screenshots/bitcoind-ncurses-tx.png)
![ScreenShot](/screenshots/bitcoind-ncurses-peers.png)
![ScreenShot](/screenshots/bitcoind-ncurses-wallet.png)
![ScreenShot](/screenshots/bitcoind-ncurses-net.png)
![ScreenShot](/screenshots/bitcoind-ncurses-console.png)

* produced by Amphibian (azeteki, Atelopus_zeteki).
* ported for darkcoind by Vertoe (vertoe).


dependencies
------------

* tested with python 2.7.9, darkcoind 0.11.0.0
* jgarzik's bitcoinrpc library port for darkcoin (https://github.com/vertoe/python-darkcoinrpc)
* chaeplin's darkcoin subsidy library, latest version by vertoe (https://github.com/vertoe/darkcoin_subsidy)
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

* mean block size/tx count over last X blocks
* transaction creation support (if I feel suicidal)
* more testing for edge cases (paramount for above)


frog food
---------

found bitcoind-ncurses useful? donations are your way of showing that! (donations for Amphibian, author of bitcoind-ncurses, of course.)

his main machine is currently a 6 year old Atom laptop. upgrading that would be rather useful. cheers!

![ScreenShot](/screenshots/donation-qr.png)

**1FrogqMmKWtp1AQSyHNbPUm53NnoGBHaBo**
