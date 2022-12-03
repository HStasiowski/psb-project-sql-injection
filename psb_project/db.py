import configparser
import logging

import pandas as pd
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
        """User login query (with injection)

        :param username:
        :param password:
        :return: (bool, bool, str) : Logged in?, With error?, Error message
        """
        ret_text = ""
        cur = self.conn.cursor()
        try:
            cur.execute(f"SELECT * "
                        f"FROM dellstore2.public.customers "
                        f"WHERE username='{username}' AND password='{password}';")
        except Exception as e:
            ret_text = str(e)
            logging.error(str(e))
            return False, True, ret_text
        else:
            ans = cur.fetchone()
            cur.close()
            logging.debug(f"Login as {username=} {password=}")
            if ans is None:
                return False, False, ret_text
            else:
                return True, False, ret_text

    def get_products(self, user_query: str):
        ret_text = ""
        sql_query = sqlalchemy.text(f"SELECT * "
                                    f"FROM dellstore2.public.products "
                                    f"WHERE (actor LIKE upper('%{user_query}%')) "
                                    f"   OR (title LIKE upper('%{user_query}%'));")
        try:
            df = pd.read_sql(sql_query, self.sqlalchemy_engine)
        except Exception as e:
            ret_text = str(e)
            logging.error(str(e))
            return pd.DataFrame(), True, ret_text
        else:
            logging.debug(f"Search result: {df.shape=}")
            return df, False, ret_text


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    db = DellStoreDB()
    db.connect(**config["postgresql-dellstore2"])
    # print(db.get_user("user12", "password"))
    print(db.get_products("alaska')) or TRUE; -- "))
    db.disconnect()
