import psycopg2

from settings import *


def get_connection():
    return psycopg2.connect("host={0} dbname={1} user={2} password={3}".format(host, db_name, username, password))
