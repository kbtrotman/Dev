
import datetime

from configparser import SafeConfigParser
from sqlalchemy import create_engine
from sqlalchemy import text
from ping3 import ping

#   Constants
CONF_FILE = "/var/www/portal-scripts/pingable.ini"
fields = "host_name, host_ip, host_serial, host_type, host_ping_ip, host_ping_name, host_ping_lat, ip_ping_lat, datetime"

db_string = "postgresql+psycopg2://operations:Postgres!909@ricbackuputil.martinmarietta.com:5432/operations"
db = create_engine(db_string)

presentDate = datetime.datetime.now()
now_epoch = datetime.datetime.timestamp(presentDate)*1000

#Subroutines

def ps_conn():
    """ Connect to the PostgreSQL database server to write the ping results """
    with db.connect() as connection:
        try:
            # read connection parameters
            result = connection.execute(text('SELECT version()'))
            print("Result:" + str(result.rowcount))
            ##db_version = connection.fetchone()
            ##print(db_version)
        except:
            print("Exception {} occurred while opening the Postgres DB!".format(ConnectionError))
    return result


def read_config():
    # create a parser
    parser = SafeConfigParser()
    parser.read(CONF_FILE)
    # get section
    for section_name in parser.sections():
        pingable = ping_test(section_name)
        ip = parser.get(section_name, "IP")
        ip_pingable = ping_test(ip)
        serial = parser.get(section_name, "SERIAL")
        hw_type = parser.get(section_name, "HWTYPE")
        db_write_results(section_name, pingable, ip, ip_pingable, serial, hw_type)
    return

def ping_test(host):
    """
    Returns True if host (str) responds to a ping request.
    """
    r = ping(host, timeout=5, unit="ms",  )

    if r is None:
        return False
    elif r == False:
        return False
    else:
        return r


def db_write_results(name, ping, ip, ip_ping, serial, hw_type):
    with db.connect() as connection:
        print("inserting new row->")
        ###fields = "host_name, host_ip, host_serial, host_type, host_ping_ip, host_ping_name, host_ping_lat, ip_ping_lat"
        if ping != False:
            host_up = True
        else:
            host_up = False
            ping = 0
        if ip_ping != False:
            ip_up = True
        else:
            ip_up = False
            ip_ping = 0
        query = "INSERT INTO host_ping (" + str(fields) + ") VALUES ('" + str(name) + "', '" + str(ip) + "', '" + str(serial) + "', '" + str(hw_type) + "', '" + str(ip_up) + "', '" + \
            str(host_up) + "', '" + str(ping) + "', '" + str(ip_ping) + "', '" + str(now_epoch) + "')"
        print("Query: " + query)
        result = connection.execute(query)
    return result

def db_disconnect():
    with db.connect() as connection:
        try:
            if connection is not None:
                connection.close()
                print('Database connection closed.')
        except:
            print("An Exception occurred while closing the Postgres DB!")
    return True


#  MAIN  ****************************************************************
if __name__ == '__main__':
    ps_conn()
    read_config()  ###  Cycle through config entries, ping hosts, and write results to DB.
    db_disconnect()
