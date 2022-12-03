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
        self.drop_db()
        cur = self.conn.cursor()
        cur.execute("CREATE DATABASE dellstore2 OWNER sqlinjection TABLESPACE dbspace;")
        cur.close()

    def fill_db(self):
        cur = self.conn.cursor()
        with open("dellstore2/dellstore2-normal-1.0.sql", "r") as sql_script:
            cur.execute(sql_script.read())
        cur.close()

    def drop_db(self):
        cur = self.conn.cursor()
        cur.execute("DROP DATABASE IF EXISTS dellstore2;")
        cur.close()

    def row_exists(self, username: str, password: str):
        cur = self.conn.cursor()
        cur.execute(f"SELECT * "
                    f"FROM dellstore2.public.customers "
                    f"WHERE username='{username}' AND password='{password}';")
        ans = cur.fetchone()
        print(ans)
        cur.close()
        logging.debug(f"Login as {username=} {password=}")
        if ans is None:
            return False
        else:
            return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    db = DellStoreDB()
    db.connect(**config["postgresql-postgres"])
    db.create_db()
    print("Success")
    db.disconnect()
