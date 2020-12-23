import psycopg2
from connection_config import connection_config


class DB:
    def __init__(self):
        self.connection = self.connect_data_base()

    def connect_data_base(self):
        connection = psycopg2.connect(connection_config)