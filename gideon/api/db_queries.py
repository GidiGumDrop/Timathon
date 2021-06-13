import sqlite3
import os


def insert_user(conn, data):
    
    sql = "INSERT INTO users(fname, sname, dob, email, password, user_pfp) VALUES (?,?,?,?,?,?);"
    
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit() 


def insert_event(conn, data):
    
    sql = "INSERT INTO events(user_id, event_title, event_desc, event_datetime, event_tags, event_agegroup, event_lat, event_lon, event_imgs) VALUES (?,?,?,?,?,?,?,?,?) returning *;"
    user_data = get_user_data(conn, str(data[0]))
    #attending_data = check_if_attending(conn, (data[0], ))

    if user_data:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        result = cur.fetchall()
        return (True, result) 
    else:
        return False


def check_if_attending(conn, data):
    
    sql = f"SELECT EXISTS(SELECT * FROM attending WHERE user_id={data[0]} AND event_id={data[1]}"
    
    curr = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    if result[0][0] == 1:
        return True
    return False
    

def add_attendance(conn, data):
    
    sql_insert = "INSERT INTO attending(user_id, event_id) VALUES(?,?);"
    
    if result[0][0] == 0 and not check_if_attending:
        cur.execute(sql_insert, data)
        conn.commit()
        return True
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
    
    
def update_user_data(conn, data):
    
    sql = f"UPDATE users SET fname='{data['fname']}', sname='{data['sname']}', dob='{data['dob']}', email='{data['email']}', password='{data['password']}', user_pfp='{data['user_pfp']}' WHERE id={data['user_id']};"
    
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def update_event_data(conn, data):
    
    sql = f"UPDATE events SET event_title='{data['title']}', event_desc='{data['desc']}', event_datetime='{data['datetime']}', event_tags='{data['tags']}', event_lat={data['lat']}, event_lon={data['lon']}, event_agegroup='{data['agegroup']}', event_imgs='{data['imgs']}' WHERE id={data['event_id']} AND user_id={data['user_id']};"
    
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
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