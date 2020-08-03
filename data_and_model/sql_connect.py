import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_filewh
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_tasks(conn,sqlquery):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
  
    cur = conn.cursor()
    try:
    	cur.execute(sqlquery)
    except Error as e:
    	print(e)	
    rows = cur.fetchall()

    for row in rows:
        print(row)
        
db_file=r"playground.db"        
conn[0]=create_connection(db_file) 
#select_all_tasks(conn[0],"SELECT (Profit) FROM `company` WHERE project  = 10475")         
