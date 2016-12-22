import socket
import sys
import re
from utils import *

url = re.compile(r".*(http\:\/\/.*?)[\;\s]")

s_addr = (sys.argv[1], int(sys.argv[2]))

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(s_addr)
print "binding socket on port:", sys.argv[2]

sock.listen(1)

while True:
        print "waiting for connection"
        connection, client_addr = sock.accept()
        try:
                country = get_country(client_addr[0])
                print "connection from:", client_addr, "country: ", country, "on port:", sys.argv[2]
                insert_into_db(sys.argv[2], client_addr[0], country, str(client_addr[1]), "")
                while True:
                        data = connection.recv(1024)
                        if data:
                                insert_into_db(sys.argv[2], client_addr[0], country, str(client_addr[1]), str(data))
                                print data
                                u = url.match(data)
                                if u != None:
                                        print "found URL:", u.groups()[0]
                        else:
                                break
        finally:
                connection.close()
