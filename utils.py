import geoip2.database, _mysql, ConfigParser

conf = ConfigParser.ConfigParser()
conf.read('./config.cfg')

geoip = conf.get("geodb", "GeoDB")
geodb = geoip2.database.Reader(geoip)

db=_mysql.connect(host=conf.get("honeydb", "DbHost"),user=conf.get("honeydb", "DbUser"),passwd=conf.get("honeydb", "DbPasswd"),db=conf.get("honeydb", "DbName"))

def get_country(ip):
        country=""
        try:
                country = geodb.country(ip).country.iso_code
        except geoip2.errors.AddressNotFoundError:
                country = "Unknown"
        return country

def insert_into_db(srvport, saddr, scountry, sport, data):
        query = "insert into connections (time, server_port, source_address, source_country, source_port, data) values (now(), "+srvport+", '"+saddr+"', '"+scountry+"', "+sport+", '"+str(data)+"')"
        db.query(query)
        db.store_result()

def get_static_ports():
        static_ports = set()
        ports = conf.get("honeyconf","StaticPorts")
        for port in ports.split(","):
                static_ports.add(int(port))
        return static_ports

def get_log_others():
        return int(conf.get("honeyconf","LogOthers"))

def get_srv_ip():
        return conf.get("honeyconf","ServerIP")
