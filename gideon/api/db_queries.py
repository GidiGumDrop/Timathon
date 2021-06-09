import sqlite3
import os


def insert_user(conn, data):
    
    sql = "INSERT INTO users(fname, sname, email, password) VALUES (?,?,?,?);"
    
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit() 


def insert_event(conn, data):
    
    sql = "INSERT INTO events(user_id, event_title, event_desc, event_datetime, tags, event_lat, event_lon) VALUES (?,?,?,?,?,?,?);"
    user_data = get_user_data(conn, str(data[0]))
    if user_data:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        return True
    else:
        return False

def get_user_data(conn, data):
    
    sql = "SELECT * FROM users WHERE id=" + data + ";"
    
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()
    

def get_user_events(conn, data):
    
    sql = "SELECT * FROM events WHERE user_id=" + data + ";"
    
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()
    

def get_conn():
    DIR_PATH = os.path.dirname(os.path.realpath(__file__+'\..'))
    db_path = DIR_PATH + '\db.db'
    conn = None
    try:
        conn = sqlite3.connect(db_path)
    except Error as e:
        return e
    return conn


def get_db_path():
    DIR_PATH = os.path.dirname(os.path.realpath(__file__+'\..'))
    db_path = DIR_PATH + '\db.db'
    return db_path
    