# this file contains the functions for db interactions
import os
import sqlite3
from sqlite3 import Error
from datetime import datetime

sql_cols = ["id","time", "job_num", "macfile_loc", "img_dir", "n_imgs", "status_str"]

construct_tbl_sql = f"""
CREATE TABLE IF NOT EXISTS work_log (
    id INTEGER PRIMARY KEY,
    {sql_cols[1]} TEXT NOT NULL,
    {sql_cols[2]} INTEGER NOT NULL,
    {sql_cols[3]} TEXT NOT NULL,
    {sql_cols[4]} TEXT NOT NULL,
    {sql_cols[5]} INTEGER NOT NULL,
    {sql_cols[6]} TEXT NOT NULL
);"""

insert_row_sql = f"""
INSERT INTO work_log ({sql_cols[1]}, {sql_cols[2]}, {sql_cols[3]}, {sql_cols[4]}, {sql_cols[5]}, {sql_cols[6]})
VALUES ('{"{}"}', {"{}"}, '{"{}"}', '{"{}"}', {"{}"}, '{"{}"}');
"""

retreive_row_sql = """
SELECT * FROM work_log ORDER BY time DESC LIMIT 1;
"""

def get_last_run_status(db_file):
    # This function checks the last run status and returns a dictionary 
    # consisting of the last run status according to the MaIDe DB structure.
    # If this is the first time maide_file_loc was constructed or could not 
    # find the database, it constructs it and returns an empty dict.
    
    # if the db does not exist, create it
    if not os.path.exists(db_file):
        with open(db_file, "w+") as f:
            pass
    # check if the table exists, create it if it does not
    con = sql_connection(db_file)
    if not check_table_exists(con):
        print("table not found, creating...")
        create_table(con, construct_tbl_sql)
    recent_row = get_most_recent_row(con)
    if con:
        con.close()
    row_dict = {sql_cols[i]:recent_row[0][i] for i in range(len(sql_cols))}
    return row_dict

def insert_run_status(db_file, job_num, macfile_loc="", img_dir="", n_imgs=0, status_str="default param"):
    # this function inserts the run status into the database
    # this function assumes the database exists and the table exists (just make sure the above method was run b4)
    # this function returns True if the insert was successful, False if not
    try:
        con = sql_connection(db_file)
        insert_row(con, job_num, macfile_loc, img_dir, n_imgs, status_str)
        if con:
            con.close()
        return True
    except Error:
        print(Error)
        return False

def check_table_exists(con):
    # this function expects db_file to exist on the system (raises error if not)
    # function returns true if the table work_log exists, false if it does not
    c = con.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='work_log';")
    return len(c.fetchall()) > 0

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

def get_most_recent_row(con):
    # This function returns the most recent row from the database
    try:
        c = con.cursor()
        c.execute(retreive_row_sql)
        return c.fetchall()
    except Error:
        print(Error)
        
def insert_row(con, job_num, macfile_loc="", img_dir="", n_imgs=0, status_str="default param"):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    my_query = insert_row_sql.format(time, job_num, macfile_loc, img_dir, n_imgs, status_str)
    try:
        c = con.cursor()
        c.execute(my_query)
        con.commit()
    except Error:
        print(Error)