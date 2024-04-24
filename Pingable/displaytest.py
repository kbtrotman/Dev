import re
import datetime

import cherrypy
cherrypy.config.update("cherrypy.config")
from jinja2 import Environment, FileSystemLoader
from configparser import SafeConfigParser
from sqlalchemy import create_engine
from sqlalchemy import text

global records
global jobs
conf_hosts = []

CONF_FILE = "/var/www/portal-scripts/pingable.ini"
db_string = "postgresql+psycopg2://operations:POSTGRES!PASSWD!HERE@webbackuputil.mycompany.com:5432/operations"
db = create_engine(db_string)
presentDate = datetime.datetime.now()
now_epoch = datetime.datetime.timestamp(presentDate)*1000

## engine = create_engine('mssql+pyodbc://' + server + '/' + database + '?trusted_connection=yes&driver=ODBC+Driver+13+for+SQL+Server')
def is_match(regex, text):
    pattern = re.compile(regex)
    return pattern.search(text) is not None


def read_config():
    # create a parser
    parser = SafeConfigParser()
    parser.read(CONF_FILE)
    # get section
    for section_name in parser.sections():
        ##pingable = ping_test(section_name)
        conf_hosts.append(section_name)
    return

def get_table_data():
    d, a, b = {}, [], []

    with db.connect() as connection:
        for host in conf_hosts:
            query = "SELECT * FROM host_ping where host_name = '" + host + "' order by datetime desc limit 1 "
            print(query)
            result = connection.execute(query)
            print("Result:")
            print(result)
            for row in result:

                for column, value in row.items():
                    print(column, value)
                    # build up the dictionary
                    d = {**d, **{column: value}}
                a.append(d)
        result = connection.execute(text("SELECT * FROM jobs where groupname not like '%Plant_Auto%' "))
        print("Result:")
        print(result)
        for row in result:
            for column, value in row.items():
                # build up the dictionary
                d = {**d, **{column: value}}
            b.append(d)
        print("B:")
        print(b)

    return a, b

class Operations(object):
    @cherrypy.expose
    def index(self):
        templateLoader = FileSystemLoader(searchpath="./templates")
        templateEnv = Environment(loader=templateLoader)
        TEMPLATE_FILE = "index.jinja"
        template = templateEnv.get_template(TEMPLATE_FILE)
        print(records)
        print(jobs)
        outputText = template.render({"records": records,"jobs": jobs,})  # this is where to put args to the template renderer
        return outputText

if __name__ == '__main__':
    read_config()
    records, jobs = get_table_data()
    css_handler = cherrypy.tools.staticdir.handler(section="/", dir='/var/www/html/portal/public/css')
    image_handler = cherrypy.tools.staticdir.handler(section="/", dir='/var/www/html/portal/public/images')
    cherrypy.tree.mount(css_handler, '/css')
    cherrypy.tree.mount(image_handler, '/images')
    cherrypy.quickstart( Operations())
