import sqlite3
import os


def insert_user(conn, data):
    
    sql = "INSERT INTO users(fname, sname, dob, email, password, user_pfp) VALUES (?,?,?,?,?,?);"
    
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit() 


def insert_event(conn, data):
    
    sql = "INSERT INTO events(user_id, event_title, event_desc, event_datetime, event_tags, event_agegroup, event_max_ppl, event_lat, event_lon, event_imgs) VALUES (?,?,?,?,?,?,?,?,?,?);"
    user_data = get_user_data(conn, str(data[0]))

    if user_data:
        cur = conn.cursor()
        cur.execute(sql, data)
        conn.commit()
        result = cur.fetchall()
        event_id = cur.lastrowid
        add_attendance(conn, (data[0], event_id))
        return True
    else:
        return False


def check_if_attending(conn, data):
    
    sql = f"SELECT EXISTS(SELECT * FROM attending WHERE user_id={data[0]} AND event_id={data[1]});"
    
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    if result[0][0] == 1:
        return True
    return False
    

def count_of_attending(conn, data):
    
    sql = f"SELECT COUNT(*) FROM attending WHERE event_id = {data};"
    
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()
    

def add_attendance(conn, data):
    
    sql_insert = "INSERT INTO attending(user_id, event_id) VALUES(?,?);"
    sql_check_max_ppl = f"SELECT event_max_ppl FROM events WHERE id = {data[1]};"
    
    cur = conn.cursor()
    cur.execute(sql_check_max_ppl)
    max_ppl = cur.fetchall()[0][0]
    
    if not check_if_attending(conn, (data[0], data[1])) and not count_of_attending(conn, data[1])[0][0] >= max_ppl:
        cur.execute(sql_insert, data)
        conn.commit()
        return True
    return False
        

def get_user_data(conn, data):
    
    sql = "SELECT * FROM users WHERE id=" + data + ";"
    
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()
    

def get_user_created_events(conn, data):
    
    sql = "SELECT * FROM events WHERE user_id=" + data + ";"
    
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def get_user_events_attending(conn, data):
    
    sql = f"SELECT * FROM events INNER JOIN attending ON attending.event_id = events.id WHERE events.user_id = {data};"
    
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
    

def search_for_events(conn, data):
    
    search_types_tup = ('agegroup', 'date', 'keywords', 'location', 'tags', 'time')
    base_sql = f"SELECT * FROM events WHERE event_datetime > datetime('now')"
    filter_list = ["event_agegroup = '{}'", "date(event_datetime) = '{}'", "event_title LIKE '%{}%'",
        "event_lat BETWEEN {0}-0.075 AND {0}+0.075 AND event_lon BETWEEN {1}-0.075 AND {1}+0.075",
        "event_tags LIKE '%{}%'", "time(event_datetime) = '{}'"]

    filter_str = ""

    if 'agegroup' in data.keys():
        filter_str += " AND " + (filter_list[0].format(data['agegroup']))
    if 'date' in data.keys():
        filter_str += " AND " + (filter_list[1].format(data['date']))
    if 'keywords' in data.keys():
        filter_str += " AND " + (filter_list[2].format(data['keywords']))
    if 'location' in data.keys():
        filter_str += " AND " + (filter_list[3].format(data['location'][0], data['location'][1]))
    if 'tags' in data.keys():
        filter_str += " AND " + (filter_list[4].format(data['tags']))
    if 'time' in data.keys():
        filter_str += " AND " + (filter_list[5].format(data['time']))

    if not filter_str == "":
        base_sql = base_sql + filter_str

    cur = conn.cursor()
    cur.execute(base_sql)
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