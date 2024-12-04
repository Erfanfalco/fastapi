import psycopg2
import logging
from typing import Optional

from termcolor import colored

from protocols import ConnectionLike, CursorLike


class DatabaseConnection:

    def __init__(self, config):
        self.config = config
        self.connection = None
        self.autocommit = True

    def connect(self, section):
        """Establishes a connection to the database."""
        try:
            host = self.config.get(section, 'host')
            dbname = self.config.get(section, 'dbname')
            user = self.config.get(section, 'user')
            password = self.config.get(section, 'password')
            port = self.config.get(section, 'port')
            self.connection = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
            logging.info(colored(f"{section} Database connection established.", "light_grey", force_color=True))
        except Exception as e:
            logging.error(f"Failed to establish database connection: {e}")
            raise

    def get_connection(self) -> ConnectionLike:
        return self.connection

    def close(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed.")

    def get_cursor(self) -> Optional[CursorLike]:
        """Returns a new cursor object."""
        if self.connection:
            return self.connection.cursor()
        else:
            logging.error("No active database connection.")
            return None
