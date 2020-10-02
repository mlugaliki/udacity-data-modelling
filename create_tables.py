import traceback

from database_connection import *
from settings import *
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """

    try:
        # connect to default database
        conn = psycopg2.connect("host={0} user={1} password={2}".format(host, username, password))
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        # create sparkify database with UTF8 encoding
        cur.execute("DROP DATABASE IF EXISTS {}".format(db_name))
        cur.execute("CREATE DATABASE {} WITH ENCODING 'utf8' TEMPLATE template0".format(db_name))

        # close connection to default database
        conn.close()

        # connect to sparkify database
        conn = get_connection()
        cur = conn.cursor()
        return cur, conn
    except Exception as e:
        traceback.print_exc()
    return None, None


def drop_tables(cur, conn):
    """
    Drops each table using the queries in `drop_table_queries` list.
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates each table using the queries in `create_table_queries` list.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    - Drops (if exists) and Creates the sparkify database.

    - Establishes connection with the sparkify database and gets
    cursor to it.

    - Drops all the tables.

    - Creates all tables needed.

    - Finally, closes the connection.
    """
    cur, conn = create_database()
    if cur is not None and conn is not None:
        drop_tables(cur, conn)
        create_tables(cur, conn)
        conn.close()


if __name__ == "__main__":
    main()
