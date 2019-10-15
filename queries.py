import os
# import sys
import sqlite3
import pandas as pd

def create_connection(DB_PATH):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(DB_PATH)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
        conn = None
    return conn


def get_df(connection, table_name):
    sql_2 = f'SELECT * FROM {table_name}'

    table_df = pd.read_sql_query(sql_2, connection)

    return table_df