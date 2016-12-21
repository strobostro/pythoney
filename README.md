# pythoney
A simple tool to create passive honeypots.

The basic idea behind pythoney is to dynamically open a TCP listener when a port is requested.

Pythoney (pythoney.py) is based on iptables nfqueue and scapy :
  - nfqueue delegates filtering decisions to a userland program
  - scapy is used to sort TCP syn from other packets and get information about the incoming packets, especially the destination port

When a SYN packet is received, it is parsed to get the destination port which is checked against two sets:
  - the set of static ports (already bound on the system be they regular services or static honeypots)
  - the set of ports that have already been dynamically opened (no need to recreate the associated listener)

The default TCP listener (server.py) opens a socket on the requested port and start recording incoming connections and payloads to a mysql database (created using the db.sql file).

# installation
Get all necessary python dependencies:
  - netfilterqueue
  - geoip2.database 
  - mysql connector
  - scapy
  
Install a MySQL server and create the pythoney database ("source db.sql").

# how to run
~/Pythoney$ sudo python pythoney.py -h
usage: pythoney.py [-h] geodbpath serverip log_other

positional arguments:
  geodbpath   file path to the GeoLite2-Country database
  serverip    IP of the interface to which services will be bounded
  log_other   switch to instruct pythoney to log connection to static services

optional arguments:
  -h, --help  show this help message and exit
  
In addition to database logging, pythoney outputs some information on the standard output.
