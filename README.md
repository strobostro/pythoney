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
