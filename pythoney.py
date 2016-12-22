from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP,TCP
import subprocess,time
import geoip2.database, _mysql,re
from utils import *

listen_addr = get_srv_ip()
log_other = get_log_others()

dyn_ports=set()         # used to store the list of ports dynamically opened (dynamic tcp listeners honeypots)

static_ports = get_static_ports()

subprocess.Popen(["iptables", "-A" ,"INPUT", "-d", listen_addr, "-j", "NFQUEUE", "--queue-num", "1"])

def print_and_accept(pkt):
        p=IP(pkt.get_payload())
        try:
                flag = p[TCP].sprintf("%flags%")
                if flag == 'S':
                        honeyport = p[TCP].dport
                        if (honeyport not in dyn_ports and honeyport not in static_ports):
                                subprocess.Popen(["python", "/home/honeydrive/Pythoney/server2.py", listen_addr, str(honeyport), geoip])
                                dyn_ports.add(honeyport)
                                time.sleep(0.5)
                        else:
                                if log_other == 1:
                                        country = get_country(p[IP].src)
                                        print "connection from:", p[IP].src, "country: ", country, "on port:", p[TCP].dport
                                        insert_into_db(str(p[TCP].dport), p[IP].src, country, str(p[TCP].sport), "")
                pkt.accept()
        except IndexError:
                pkt.accept()

nfqueue = NetfilterQueue()
nfqueue.bind(1, print_and_accept)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print "exiting pythoney"
