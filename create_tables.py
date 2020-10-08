import traceback

import psycopg2
from sql_queries import create_table_queries, drop_table_queries, drop_database, recreate_database


def create_database():
    """
    - Creates and connects to the sparkifydb
    - Returns the connection and cursor to sparkifydb
    """

    try:
        # connect to default database
        conn = psycopg2.connect("host=127.0.0.1 user=postgres password=postgres")
        conn.set_session(autocommit=True)
        cur = conn.cursor()

        # create sparkify database with UTF8 encoding
        cur.execute(drop_database)
        cur.execute(recreate_database)

        # close connection to default database
        conn.close()

        # connect to sparkify database
        conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=postgres")
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
