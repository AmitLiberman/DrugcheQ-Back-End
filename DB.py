import psycopg2
from connection_config import connection_config


class DB:
    def __init__(self):
        self.connection = self.connect_data_base()

    def connect_data_base(self):
        connection = psycopg2.connect(connection_config)
        return connection

    def creat_table(self):
        with self.connection as connect:
            cur = connect.cursor()

    def close_connection(self):
        self.connection.close()

    def fetch_all_data(self, query, value):
        with self.connection as conn:
            cur = conn.cursor()
            if value:
                cur.execute(query, (value,))
            else:
                cur.execute(query)
            return cur.fetchall()
