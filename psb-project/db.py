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

    def connect(self):
        """Connect to the PostgreSQL database server."""
        try:
            logging.info("Connecting to the PostgreSQL database...")
            self.conn = psycopg2.connect(**config["postgresql"])
            self.sqlalchemy_engine = sqlalchemy.create_engine(
                'postgresql+psycopg2://',
                creator=lambda: self.conn)

            # Display PostgreSQL version
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

    def row_exists(self, key_value: Any, key_column: str, table: str):
        """Checks whether there is a record with
        the same `key_value` in the specified `table`."""
        cur = self.conn.cursor()
        query = (f"SELECT {key_column} "
                 f"FROM   {table} "
                 f"WHERE  {key_column} = %s;")
        cur.execute(query, (key_value,))
        ans = cur.fetchone()
        cur.close()
        logging.debug(f"Check if exists {key_column=} {key_value=} in {table}"
                      f"Response {True if ans is not None else False}.")
        if ans is None:
            return False
        else:
            return True


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    db = DellStoreDB()
    db.connect()
    print("Success")
    db.disconnect()
