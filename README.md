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
  - netfilterqueue (http://pypi.python.org/packages/source/N/NetfilterQueue/NetfilterQueue-0.3.tar.gz)
  - geoip2.database (python-geoip on Debian GNU Linux) + country database (http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.mmdb.gz)
  - mysql connector (python-mysqldb on Debian GNU Linux)
  - scapy (python-scapy on Debian GNU Linux)
  
Install a MySQL server and create the pythoney database ("source db.sql").

# configuration
There is a global configuration file to pythoney, called "config.cfg", parsed with ConfigParser.

[honeyconf]
ServerIP = < the ip address of the interface on which honeypot services will be bounded>
LogOthers = [0 | 1] < default is 0 - a switch that instructs pythoney to also log into the database the connection to ports declared as static, ie. not usable as dynamic honeypot ports because they are already bounded >
StaticPorts = 23, 80 < a list of ports to be considered as static - see explanation above >

[honeydb] < connection details to the python myqsl database >
DbHost = localhost  
DbName = pythoney
DbUser = pythoney
DbPasswd = pythoney

[geodb] < the path to the geolite2 country database >
GeoDB = < some_path >


# how to run
:~/Pythoney$ sudo python pythoney.py 
binding socket on port: 7547
waiting for connection
binding socket on port: 5555
waiting for connection
connection from: (< ip >, 26437) country:  CZ on port: 1234
connection from: (< ip >, 26438) country:  CZ on port: 5678
  
In addition to database logging, pythoney outputs some information on the standard output.

:~/Pythoney$ mysql -u pythoney -p -D pythoney

Enter password: 

[...]

mysql> desc connections;

+----------------+---------------+------+-----+-------------------+-----------------------------+

| Field          | Type          | Null | Key | Default           | Extra                       |

+----------------+---------------+------+-----+-------------------+-----------------------------+

| id             | int(11)       | NO   | PRI | NULL              | auto_increment              |

| time           | timestamp     | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |

| server_port    | int(11)       | YES  |     | NULL              |                             |

| source_address | varchar(16)   | YES  |     | NULL              |                             |

| source_country | varchar(8)    | YES  |     | NULL              |                             |

| source_port    | int(11)       | YES  |     | NULL              |                             |

| data           | varchar(1024) | YES  |     | NULL              |                             |

+----------------+---------------+------+-----+-------------------+-----------------------------+

7 rows in set (0.02 sec)

mysql> select count(*) from connections;

+----------+

| count(*) |

+----------+

|      201 |

+----------+

1 row in set (0.00 sec)


mysql> select distinct(source_country) from connections;


+----------------+

| source_country |

+----------------+

| TR             |

| TW             |

| PR             |

| TH             |

[...]
