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

    def insert_row(self, query, data):
         with self.connection as conn:
            cur = conn.cursor()
            try:
                # postgres_insert_query = """ INSERT INTO mobile (ID, MODEL, PRICE) VALUES (%s,%s,%s)"""
                postgres_insert_query = query
                # record_to_insert = (5, 'One Plus 6', 950)
                cur.execute(postgres_insert_query, data)

                conn.commit()
                count = cur.rowcount
                print(count, "Record inserted successfully into mobile table")

            except (Exception, psycopg2.Error) as error:
                print("Failed to insert record into mobile table", error)
