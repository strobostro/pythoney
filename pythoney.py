from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP,TCP
import subprocess,time
import geoip2.database, _mysql,re
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("geodbpath", help="file path to the GeoLite2-Country database", type=str)
parser.add_argument("serverip", help="IP of the interface to which services will be bounded", type=str)
parser.add_argument("log_other", help="switch to instruct pythoney to log connection to static services", type=int)
args = parser.parse_args()

geoip = args.geodbpath
listen_addr = args.serverip
log_other = args.log_other

geodb = geoip2.database.Reader(geoip)

db=_mysql.connect(host="localhost",user="pythoney",passwd="pythoney",db="pythoney")

dyn_ports=set()         # used to store the list of ports dynamically opened (dynamic tcp listeners honeypots)
static_ports=set()      # used to store the list ports used by static honeypots

static_ports.add(23)
static_ports.add(80)

subprocess.Popen(["iptables", "-A" ,"INPUT", "-d", listen_addr, "-j", "NFQUEUE", "--queue-num", "1"])

def print_and_accept(pkt):
        p=IP(pkt.get_payload())
        try:
                flag = p[TCP].sprintf("%flags%")
                if flag == 'S':
                        honeyport = p[TCP].dport
                        if (honeyport not in dyn_ports and honeyport not in static_ports):
                                subprocess.Popen(["python", "/home/honeydrive/Pythoney/server.py", listen_addr, str(honeyport)])
                                dyn_ports.add(honeyport)
                                time.sleep(0.5)
                        else:
                                if log_other == 1:
                                        try:
                                                country = geodb.country(p[IP].src).country.iso_code
                                        except geoip2.errors.AddressNotFoundError:
                                                country = "Unknown"
                                        print "connection from:", p[IP].src, "country: ", country, "on port:", p[TCP].dport
                                        query = "insert into connections (time, server_port, source_address, source_country, source_port) values (now(), "+ str(p[TCP].dport)+", '"+p[IP].src+"', '"+country+"', "+str(p[TCP].sport)+")"
                                        db.query(query)
                                        db.store_result()
                pkt.accept()
        except IndexError:
                pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print "exiting pythoney"
