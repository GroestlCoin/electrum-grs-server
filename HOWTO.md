How to run your own Electrum-GRS server
===================================

Abstract
--------

This document is an easy to follow guide to installing and running your own
Electrum-GRS server on Linux. It is structured as a series of steps you need to
follow, ordered in the most logical way. The next two sections describe some
conventions we use in this document and the hardware, software, and expertise
requirements.

The most up-to date version of this document is available at:

    https://github.com/Groestlcoin/electrum-grs-server/blob/master/HOWTO.md

Conventions
-----------

In this document, lines starting with a hash sign (#) or a dollar sign ($)
contain commands. Commands starting with a hash should be run as root,
commands starting with a dollar should be run as a normal user (in this
document, we assume that user is called 'electrum-grs'). We also assume the
electrum-grs user has sudo rights, so we use '$ sudo command' when we need to.

Strings that are surrounded by "lower than" and "greater than" ( < and > )
should be replaced by the user with something appropriate. For example,
\<password\> should be replaced by a user chosen password. Do not confuse this
notation with shell redirection ('command < file' or 'command > file')!

Lines that lack hash or dollar signs are pastes from config files. They
should be copied verbatim or adapted without the indentation tab.

apt-get install commands are suggestions for required dependencies.
They conform to an Ubuntu 13.10 system but may well work with Debian
or earlier and later versions of Ubuntu.

Prerequisites
-------------

**Expertise.** You should be familiar with Linux command line and
standard Linux commands. You should have a basic understanding of git
and Python packages. You should have knowledge about how to install and
configure software on your Linux distribution. You should be able to
add commands to your distribution's startup scripts. If one of the
commands included in this document is not available or does not
perform the operation described here, you are expected to fix the
issue so you can continue following this howto.

**Software.** A recent Linux 64-bit distribution with the following software
installed: `python`, `easy_install`, `git`, standard C/C++
build chain. You will need root access in order to install other software or
Python libraries. Python 2.7 is the minimum supported version.

**Hardware.** The lightest setup is a pruning server with diskspace 
requirements of about 125 MB for the electrum database. However note that 
you also need to run groestlcoind and keep a copy of the full blockchain, 
which is roughly 500 MB in January 2016. If you have less than 2 GB of RAM 
make sure you limit groestlcoind to 8 concurrent connections. If you have more 
resources to spare you can run the server with a higher limit of historic 
transactions per address. CPU speed is important for the initial block 
chain import, but is also important if you plan to run a public Electrum server, 
which could serve tens of concurrent requests. Any multi-core x86 CPU from 2009 or
newer other than an Atom should do for good performance. An ideal setup
has enough RAM to hold and process the leveldb database in tmpfs (e.g. /dev/shm).

Instructions
------------

### Prepare

aptitude update -y
aptitude upgrade -y
apt-get update -y
apt-get upgrade -y
apt-get dist-upgrade -y
dd if=/dev/zero of=/swapfile bs=1M count=1024
mkswap /swapfile
swapon /swapfile
echo "/swapfile swap swap defaults 0 0" >> /etc/fstab 

### Step 1. Create a user for running groestlcoind and Electrum-grs server

This step is optional, but for better security and resource separation I
suggest you create a separate user just for running `groestlcoind` and Electrum-GRS.
We will also use the `~/bin` directory to keep locally installed files
(others might want to use `/usr/local/bin` instead). We will download source
code files to the `~/src` directory.

    $ sudo adduser electrum-grs --disabled-password
    $ sudo apt-get install git
    $ sudo su - electrum-grs
    $ mkdir ~/bin ~/src
    $ echo $PATH

If you don't see `/home/electrum-grs/bin` in the output, you should add this line
to your `.bashrc`, `.profile`, or `.bash_profile`, then logout and relogin:

    PATH="$HOME/bin:$PATH"
    $ exit

### Step 2. Download groestlcoind

    $ sudo apt-get build-essential libssl-dev libboost-all-dev libdb5.1 libdb5.1-dev libdb5.1++-dev libtool
    $ apt-get install git ntp make g++ gcc autoconf cpp ngrep iftop sysstat autotools-dev pkg-config
    $ sudo su - electrum-grs
    $ git clone https://github.com/groestlcoin/groestlcoin
    $ cd groestlcoin
    $ ./autogen.sh
    $ configure --with-incompatible-bdb
    $ make
    $ strip src/groestlcoind src/groestlcoin-cli src/groestlcoin-tx
    $ cp -a src/groestlcoind src/groestlcoin-cli src/groestlcoin-tx ~/bin

### Step 3. Configure and start groestlcoind

In order to allow Electrum-GRS to "talk" to `groestlcoind`, we need to set up an RPC
username and password for `groestlcoind`. We will then start `groestlcoind` and
wait for it to complete downloading the blockchain.

    $ mkdir ~/.groestlcoin
    $ nano ~/.groestlcoin/groestlcoin.conf

Write this in `GroestlCoin.conf`:

    rpcuser=<rpc-username>
    rpcpassword=<rpc-password>
    daemon=1
    txindex=1
    rpcallowip=127.0.0.1
    addnode=groestlcoin.org
    addnode=jswallet.groestlcoin.org
    addnode=electrum1.groestlcoin.org
    addnode=electrum2.groestlcoin.org
    rpcport=1441
    maxconnections=873
    server=1
    listen=1

If you have an existing installation of groestlcoind and have not previously
set txindex=1 you need to reindex the blockchain by running

    $ groestlcoind -reindex

If you already have a freshly indexed copy of the blockchain with txindex start `groestlcoind`:

    $ groestlcoind

Allow some time to pass for `groestlcoind` to connect to the network and start
downloading blocks. You can check its progress by running:

    $ groestlcoin-cli getinfo

Before starting the electrum server your groestlCoind should have processed all 
blocks and caught up to the current height of the network (not just the headers).
You should also set up your system to automatically start groestlcoind at boot
time, running as the 'electrum-grs' user. Check your system documentation to
find out the best way to do this.

### Step 4. Download and install Electrum-GRS Server

We will download the latest git snapshot for Electrum-GRS to configure and install it:

    $ cd ~
    $ git clone https://github.com/groestlcoin/electrum-grs-server.git
    $ cd electrum-grs-server
    $ sudo ./configure (default, default, configure rpcuser and rpcpassword)
    $ sudo python setup.py install

See the INSTALL file for more information about the configure and install commands. 

### Step 5: Install Electrum-GRS dependencies manually

Electrum-GRS server depends on various standard Python libraries and leveldb. These will usually be
installed by caling "python setup.py install" above. They can be also be installed with your
package manager if you don't want to use the install routine

    $ sudo apt-get install python-setuptools python-openssl python-leveldb libleveldb-dev 
    $ sudo easy_install jsonrpclib irc plyvel

Regarding leveldb see the steps in README.leveldb for further details, especially if your system
doesn't have the python-leveldb package or if plyvel installation fails.

leveldb should be at least version 1.9.0. Earlier version are believed to be buggy.

### Step 6. Select your limit

Electrum server uses leveldb to store transactions. You can choose
how many spent transactions per address you want to store on the server.
The default is 100, but there are also servers with 1000 or even 10000.
Few addresses have more than 10000 transactions. A limit this high
can be considered equivalent to a "full" server. Full servers previously
used abe to store the blockchain. The use of abe for electrum servers is now
deprecated.

The pruning server uses leveldb and keeps a smaller and
faster database by pruning spent transactions. It's a lot quicker to get up
and running and requires less maintenance and diskspace than abe.

The section in the electrum server configuration file (see step 10) looks like this:

     [leveldb]
     path = /path/to/your/database
     # for each address, history will be pruned if it is longer than this limit
     pruning_limit = 1000

### Step 7. Import blockchain into the database or download it

As of January 2016 it takes several hours to import 910k blocks, depending
on CPU speed, I/O speed, and your selected pruning limit.

### Step 8. Create a self-signed SSL cert

[Note: SSL certificates signed by a CA are supported by 2.0 clients.]

To run SSL / HTTPS you need to generate a self-signed certificateusing openssl. 
You could just comment out the SSL / HTTPS ports in the config and run 
without, but this is not recommended.

Use the sample code below to create a self-signed cert with a recommended validity 
of 5 years. You may supply any information for your sign request to identify your server.
They are not currently checked by the client except for the validity date.
When asked for a challenge password just leave it empty and press enter.

    $ openssl genrsa -des3 -passout pass:x -out server.pass.key 2048
    $ openssl rsa -passin pass:x -in server.pass.key -out server.key
    writing RSA key
    $ rm server.pass.key
    $ openssl req -new -key server.key -out server.csr
    ...
    Country Name (2 letter code) [AU]:US
    State or Province Name (full name) [Some-State]:California
    Common Name (eg, YOUR name) []: electrum-grs-server.tld
    ...
    A challenge password []:
    ...

    $ openssl x509 -req -days 730 -in server.csr -signkey server.key -out server.crt

The server.crt file is your certificate suitable for the ssl_certfile= parameter and
server.key corresponds to ssl_keyfile= in your electrum-grs server config.

If your certificate is lost or expires on the server side, you will need to run
your server with a different server name and a new certificate.
Therefore it's a good idea to make an offline backup copy of your certificate and key
in case you need to restore it.

### Step 9. Configure Electrum-grs server

Electrum-grs reads a config file (/etc/electrum-grs.conf) when starting up. This
file includes the database setup, bitcoind RPC setup, and a few other
options.

The "configure" script listed above will create a config file at /etc/electrum-grs.conf
which you can edit to modify the settings.

Go through the config options and configure it:
   $ sudo nano /etc/electrum-grs.conf
   $ edit bitcoind_port to 1441

If you intend to run the server publicly have a look at README-IRC.md

### Step 10. Tweak and configure your system for running electrum

Electrum-grs server currently needs quite a few file handles to use leveldb. It also requires
file handles for each connection made to the server. It's good practice to increase the
open files limit to 64k. 

The "configure" script will take care of this and ask you to create a user for running electrum-grs-server.
If you're using user electrum-grs to run electrum-grs and have added it manually like shown in this HOWTO run 
the following code to add the limits to your /etc/security/limits.conf:

     echo "groestlcoind hard nofile 65536" >> /etc/security/limits.conf
     echo "groestlcoind soft nofile 65536" >> /etc/security/limits.conf

If you are on Debian > 8.0 Jessie or other distribution based on it, you also need to add these lines in /etc/pam.d/common-session and /etc/pam.d/common-session-noninteractive otherwise the limits in /etc/security/limits.conf will not work:

    echo "session required pam_limits.so" >> /etc/pam.d/common-session
    echo "session required pam_limits.so" >> /etc/pam.d/common-session-noninteractive
    
Check if the limits are changed either by logging with the user configured to run Electrum-GRS server as. Example:

    su - electrum-grs
    ulimit -n

Or if you use sudo and the user is added to sudoers group:

    sudo -u electrum-grs -i ulimit -n


Two more things for you to consider:

1. To increase security you may want to close groestlcoind for incoming connections and connect outbound only

2. Consider restarting groestlcoind (together with electrum-grs-server) on a weekly basis to clear out unconfirmed
   transactions from the local the memory pool which did not propagate over the network.

Run also these command:
	  $ sudo chown electrum-grs /var/log/electrum-grs.log
	  $ sudo mkdir /var/electrum-grs-server
	  $ sudo chown -R electrum-grs /var/electrum-grs-server

### Step 11. (Finally!) Run Electrum-GRS server

The magic moment has come: you can now start your Electrum-GRS server as root (it will su to your unprivileged user):

    # electrum-grs-server start (or sudo su electrum-grs -c "./run_electrum_grs_server.py")

Note: If you want to run the server without installing it on your system, just run 'run_electrum_grs_server" as the
unprivileged user.

You should see this in the log file:

    starting Electrum server

If you want to stop Electrum-grs server, use the 'stop' command:

    # electrum-grs-server stop

If your system supports it, you may add electrum-grs-server to the /etc/init.d directory. 
This will ensure that the server is started and stopped automatically, and that the database is closed 
safely whenever your machine is rebooted.

    # ln -s `which electrum-grs-server` /etc/init.d/electrum-grs-server
    # update-rc.d electrum-grs-server defaults

### Step 12. Test the Electrum-grs server

We will assume you have a working Electrum-GRS client, a wallet, and some
transactions history. You should start the client and click on the green
checkmark (last button on the right of the status bar) to open the Server
selection window. If your server is public, you should see it in the list
and you can select it. If you server is private, you need to enter its IP
or hostname and the port. Press 'Ok' and the client will disconnect from the
current server and connect to your new Electrum-grs server. You should see your
addresses and transactions history. You can see the number of blocks and
response time in the Server selection window. You should send/receive some
bitcoins to confirm that everything is working properly.

### Step 13. Join us on IRC, subscribe to the server thread

Say hi to the dev crew, other server operators, and fans on 
irc.freenode.net #groestlcoin and we'll try to congratulate you
on supporting the community by running an Electrum-GRS node.

If you're operating a public Electrum-grs server please subscribe
to or regulary check the following thread:
https://bitcointalk.org/index.php?topic=525926.0
It'll contain announcements about important updates to Electrum-grs
server required for a smooth user experience.
