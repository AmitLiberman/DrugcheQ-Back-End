import psycopg2
from connection_config import connection_config


# """
# CREATE TABLE private_user_details (
#     serial SERIAL PRIMARY KEY,
#     factor_name text NOT NULL,
#     email text ,
#     phone text ,
#     sector text ,
#     medical_sector text NOT NULL,
#     real_data BOOLEAN
# )
# """,
# """
# CREATE TABLE report_details (
#     serial SERIAL PRIMARY KEY,
#     drugs text[] NOT NULL,
#     fromDate text[] NOT NULL,
#     untilDate text[] NOT NULL,
#     symptoms text[] NOT NULL,
#     severity text[]  NOT NULL,
#     appearDate text[] NOT NULL,
#     real_data BOOLEAN
# )
# """,


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (

        """
        ALTER TABLE report_details
        ADD isNew text[] ;
        """,
    )
    conn = None
    try:
        # read the connection parameters
         # connect to the PostgreSQL server
        conn = psycopg2.connect(connection_config)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # cur.execute('DROP TABLE "private_user_details";')
        # cur.execute('DROP TABLE "report_details";')

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

#
# if __name__ == '__main__':
#     create_tables()