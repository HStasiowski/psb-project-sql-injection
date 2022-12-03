import configparser
import logging
from typing import Any

import psycopg2
import sqlalchemy

config = configparser.ConfigParser()
config.read('config.ini')


class DellStoreDB:
    """ Makes the communication with the database easier."""

    def __init__(self):
        self.conn = None
        self.is_connected = False
        self.sqlalchemy_engine: sqlalchemy.engine.base.Engine | None = None

    def connect(self, **kwargs):
        """Connect to the PostgreSQL database server."""
        try:
            logging.info("Connecting to the PostgreSQL database...")
            self.conn = psycopg2.connect(**kwargs)
            self.sqlalchemy_engine = sqlalchemy.create_engine(
                'postgresql+psycopg2://',
                creator=lambda: self.conn)

            # Display PostgreSQL version
            self.conn.autocommit = True
            cur = self.conn.cursor()
            cur.execute('SELECT version()')
            logging.info(f"PostgreSQL version:\t{cur.fetchone()}")
            cur.close()

        except (Exception, psycopg2.DatabaseError):
            logging.exception('')

        if self.conn is not None:
            self.is_connected = True

    def disconnect(self):
        """Disconnect from the PostgreSQL database server."""
        if self.conn is not None:
            self.conn.close()
            self.sqlalchemy_engine.dispose()
            self.conn = None
            logging.info("Database connection closed.")
            self.is_connected = False
        else:
            # executes when there was no connection
            logging.warning("Database was asked to be closed, but there was no connection.")
            logging.warning(f"self.is_connected set to False (before it was {self.is_connected}).")
            self.is_connected = False

    def create_db(self):
        cur = self.conn.cursor()
        cur.execute("CREATE DATABASE dellstore2 OWNER sqlinjection TABLESPACE dbspace;")
        logging.info("Database dellstore2 has been created.")
        cur.close()

    def fill_db(self):
        cur = self.conn.cursor()
        logging.info("Starting to populate dellstore2 db tables with data...")
        with open("dellstore2/dellstore2-normal-1.0.sql", "r") as sql_script:
            cur.execute(sql_script.read())
        logging.info("Done.")
        cur.close()

    def drop_tables(self):
        cur = self.conn.cursor()
        cur.execute("DROP TABLE IF EXISTS public.categories ;"
                    "DROP TABLE IF EXISTS public.cust_hist; "
                    "DROP TABLE IF EXISTS public.inventory; "
                    "DROP TABLE IF EXISTS public.orderlines; "
                    "DROP TABLE IF EXISTS public.orders; "
                    "DROP TABLE IF EXISTS public.customers; "
                    "DROP TABLE IF EXISTS public.products; "
                    "DROP TABLE IF EXISTS public.reorder; "
                    "DROP FUNCTION IF EXISTS public.new_customer;")
        cur.close()


    def drop_db(self):
        cur = self.conn.cursor()
        cur.execute("DROP DATABASE IF EXISTS dellstore2;")
        logging.info("Database dellstore2 has been dropped.")
        cur.close()

    def get_user(self, username: str, password: str):
        ret_text = ""
        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT * "
                        f"FROM dellstore2.public.customers "
                        f"WHERE username='{username}' AND password='{password}';")
        except Exception as e:
            ret_text = str(e)
            logging.error(str(e))
            return False, ret_text
        else:
            ans = cur.fetchone()
            print(ans)
            cur.close()
            logging.debug(f"Login as {username=} {password=}")
            if ans is None:
                return False, ret_text
            else:
                return True, ret_text


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    db = DellStoreDB()
    db.connect(**config["postgresql-dellstore2"])
    # db.get_user("user12' &", "password")
    db.drop_tables()
    db.fill_db()
    db.disconnect()
