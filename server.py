import socket
import sys
import geoip2.database, _mysql,re

geodb = geoip2.database.Reader(sys.argv[3])

db=_mysql.connect(host="localhost",user="pythoney",passwd="pythoney",db="pythoney")

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
                try:
                        country = geodb.country(client_addr[0]).country.iso_code
                except geoip2.errors.AddressNotFoundError:
                        country = "Unknown"
                print "connection from:", client_addr, "country: ", country, "on port:", sys.argv[2]
                query = "insert into connections (time, server_port, source_address, source_country, source_port) values (now(), "+sys.argv[2]+", '"+client_addr[0]+"', '"+country+"', "+str(client_addr[1])+")"
                db.query(query)
                db.store_result()
                while True:
                        data = connection.recv(1024)
                        if data:
                                query = "insert into connections (time, server_port, source_address, source_country, source_port, data) values (now(), "+sys.argv[2]+", '"+client_addr[0]+"', '"+country+"', "+str(client_addr[1])+", '"+data+"')"
                                print data
                                db.query(query)
                                db.store_result()
                                u = url.match(data)
                                if u != None:
                                        print "found URL:", u.groups()[0]
                        else:
                                break
        finally:
                connection.close()
