# this file contains the functions for db interactions
import os
import sqlite3
from sqlite3 import Error

construct_tbl_sql = """
CREATE TABLE IF NOT EXISTS run_status (id integer PRIMARY KEY, 
                                       status text NOT NULL);)"""

def get_last_run_status(db_file):
    # This function checks the last run status and returns a dictionary 
    # consisting of the last run status according to the MaIDe DB structure.
    # If this is the first time maide_file_loc was constructed or could not 
    # find the database, it constructs it and returns an empty dict.

    

def check_db_exists(db_file):
    # function returns true if the db exists, false if it does not
    return os.path.exists(db_file)

def sql_connection(db_file):
    # This function creates a connection to the sqlite database
    # if the database does not exist, it creates it
    # if the database does exist, it returns the connection
    try:
        con = sqlite3.connect(db_file)
        return con
    except Error:
        print(Error)
    
def create_table(con, create_table_sql):
    # This function creates a table in the database
    # if the table already exists, it does nothing
    try:
        c = con.cursor()
        c.execute(create_table_sql)
    except Error:
        print(Error)