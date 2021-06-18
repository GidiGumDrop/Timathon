from flask import Flask, jsonify, request
from flask_selfdoc import Autodoc
import db_queries

app = Flask(__name__)
app.config['DEBUG'] = True
auto = Autodoc(app)


@app.errorhandler(404)
def http_not_found(e):
    return jsonify({"status": 404})


@app.route('/api/docs/', methods=['GET'])
def docs():
    return auto.html()


@app.route('/api/', methods=['GET'])
def root():
    return jsonify({"status": 200})


@app.route('/api/insert_new_user/', methods=['POST'])
@auto.doc()
def insert_new_user():

    data = request.get_json()
    if not data:
        data = {}
    req_keys = {'fname', 'sname', 'email', 'password', 'dob', 'user_pfp'}

    if data.keys() >= req_keys:
        try:
            conn = db_queries.get_conn()
            db_queries.insert_user(conn, (data['fname'], data['sname'], data['dob'], data['email'], data['password'], data['user_pfp']))
            return jsonify({"message": "success"})
        except:
            return jsonify({"message": "error"})
    else:
        return jsonify({"message": "invalid data"})
            

@app.route('/api/insert_new_event/', methods=['POST'])
@auto.doc()
def insert_new_event():
    
    data = request.get_json()
    if not data:
        data = {}
    req_keys = {'user_id', 'title', 'desc', 'datetime', 'tags', 'lat', 'lon', 'agegroup', 'max_ppl', 'imgs'}
    
    if data.keys() >= req_keys:
        try:
            conn = db_queries.get_conn()
            result = db_queries.insert_event(conn, (int(data['user_id']), data['title'], data['desc'], data['datetime'], data['tags'], data['agegroup'], int(data['max_ppl']), float(data['lat']), float(data['lon']), data['imgs']))
            if result:
                return jsonify({"message": "success"})
            else:
                return jsonify({"message": "no user with this id found"})
        except:
            return jsonify({"message": "error"})
    else:
        return jsonify({"message": "invalid data"})


@app.route('/api/insert_user_attendance/', methods=['POST'])
@auto.doc()
def insert_user_attendance():
    
    data = request.get_json()
    if not data:
        data = {}
    req_keys = {'user_id', 'event_id'}
    
    if data.keys() >= req_keys:
        try:
            conn = db_queries.get_conn()
            result = db_queries.add_attendance(conn, (data['user_id'], data['event_id']))
            if result:
                return jsonify({"message":"success"})
            return jsonify({"message":"user already attending this event or max attendance reached"})
        except:
            return jsonify({"message":"error"})
    else:
        return jsonify({"message":"invalid data"})


@app.route('/api/get_user_info/', methods=['GET'])
@auto.doc()
def get_user_info():
    
    user_id = request.args.get('user_id')
  
    if user_id:
        try:
            conn = db_queries.get_conn()
            data = db_queries.get_user_data(conn, user_id)
            if not data:
                return jsonify({"message": "no user with this id found"})

            return jsonify({"status":200, "data":{"user_id": data[0][0], "fname": data[0][1], "sname": data[0][2], "dob": data[0][3], "email": data[0][4], "password": data[0][5], "user_pfp": data[0][6]}})
        except:
            return jsonify({"message":"error"})
    else:
        return jsonify({"message": "invalid data"})


@app.route('/api/get_user_created_events/', methods=['GET'])
@auto.doc()
def get_user_created_events():
    
    user_id = request.args.get('user_id')
    
    if user_id:
        try:
            conn = db_queries.get_conn()
            data = db_queries.get_user_created_events(conn, user_id)
            
            if not data:
                return jsonify({"message": "no events for this user or no user with this id"})
                
            return_str = []
            for i in data:
                return_str.append({"event_id": i[0], "event_title": i[2], "event_desc": i[3], "event_datetime": i[4], "event_tags": i[5], "event_agegroup": i[6], "event_max_ppl":i[7], "event_lat": i[8], "event_lon": i[9], "event_imgs": i[10]})
            return_str.append({"status": 200, "user_id": user_id})
            
            return jsonify(return_str)
        except:
            return jsonify({"message": "error"})
    else:
        return jsonify({"message": "invalid data"})


@app.route('/api/get_user_attending/', methods=['GET'])
@auto.doc()
def get_user_attending():
    
    user_id = request.args.get('user_id')
    
    if user_id:
        try:
            conn = db_queries.get_conn()
            data = db_queries.get_user_events_attending(conn, user_id)
            
            if not data:
                return jsonify({"message":"this user is attending no events or this user_id is invalid"})
            
            return_str = []
            for i in data:
                return_str.append({"event_id": i[0], "event_title": i[2], "event_desc": i[3], "event_datetime": i[4], "event_tags": i[5], "event_agegroup": i[6], "event_max_ppl":i[7], "event_lat": i[8], "event_lon": i[9], "event_imgs": i[10]})
            return_str.append({"status":200, "user_id":user_id})
            
            return jsonify(return_str)
        except:
            return jsonify({"message": "error"})
    else:
        return jsonify({"message":"invalid data"})


@app.route('/api/check_if_attending/', methods=['GET'])
@auto.doc()
def check_if_attending():
    
    user_id = request.args.get('user_id')
    event_id = request.args.get('event_id')
    
    if user_id and event_id:
        
        conn = db_queries.get_conn()
        data = db_queries.check_if_attending(conn, (user_id, event_id))
        return jsonify({"attending":data})
        
        

@app.route('/api/update_user_info/', methods=['POST'])
@auto.doc()
def update_user_info():

    data = request.get_json()
    if not data:
        data = {}
    req_keys = {'user_id', 'fname', 'sname', 'email', 'password', 'dob', 'user_pfp'}
    
    if data.keys() >= req_keys:
        try:
            conn = db_queries.get_conn()
            db_queries.update_user_data(conn, data)
            return jsonify({"message":"success"})
        except:
            return jsonify({"message":"error"})
    else:
        return jsonify({"message":"invalid data"})
        

@app.route('/api/update_event_info/', methods=['POST'])
@auto.doc()
def update_event_info():

    data = request.get_json()
    if not data:
        data = {}
    req_keys = {'event_id', 'user_id', 'title', 'desc', 'datetime', 'tags', 'lat', 'lon', 'agegroup', 'imgs'}
        
    if data.keys() >= req_keys:
        try:
            conn = db_queries.get_conn()
            db_queries.update_event_data(conn, data)
            return jsonify({"message":"success"})
        except:
            return jsonify({"message":"error"})
    else:
        return jsonify({"message":"invalid data"})


@app.route('/api/delete_user/', methods=['GET'])
@auto.doc()
def delete_user():
    
    user_id = request.args.get('user_id')
    
    if user_id:
        try:
            conn = db_queries.get_conn()
            db_queries.delete_user(conn, user_id)
            return jsonify({"message":"success"})
        except:
            return jsonify({"message":"error"})
    else:
        return jsonify({"message":"ivalid data"})


@app.route('/api/delete_event/', methods=['GET'])
@auto.doc()
def delete_event():
    
    user_id = request.args.get('user_id')
    event_id = request.args.get('event_id')
    
    if user_id and event_id:
        try:
            conn = db_queries.get_conn()
            db_queries.delete_event(conn, (user_id, event_id))
            return jsonify({"message":"success"})
        except:
            return jsonify({"message":"error"})
    else:
        return jsonify({"message":"invalid data"})
        

@app.route('/api/delete_attendance/', methods=['GET'])
@auto.doc()
def delete_attendance():
    
    user_id = request.args.get('user_id')
    event_id = request.args.get('event_id')
    
    if user_id and event_id:
        try:
            conn = db_queries.get_conn()
            db_queries.delete_attendance(conn, (user_id, event_id))
            return jsonify({"message":"success"})
        except:
            return jsonify({"message":"error"})
    else:
        return jsonify({"message":"invalid data"})


@app.route('/api/search_events/', methods=['POST'])
@auto.doc()
def search_events():
    
    data = request.get_json()
    if not data:
        data = {}
    
    data = dict(sorted(data.items(), key=lambda x: x[0].lower()))
    if data == {}:
        return jsonify({"message":"invalid data"})
    
    conn = db_queries.get_conn()
    result = db_queries.search_for_events(conn, data)
    return jsonify({"data":result})
    return_str = []
    for i in data:
        return_str.append({"event_id": i[0], "user_id": i[1], "event_title": i[2], "event_desc": i[3], "event_datetime": i[4], "event_tags": i[5], "event_agegroup": i[6], "event_max_ppl":i[7], "event_lat": i[8], "event_lon": i[9], "event_imgs": i[10]})
    return_str.append({"status":200})
    return return_str

        
@app.route('/api/test/', methods=['GET', 'POST'])
def test():
    
    x = request.args.get('x')
    
    
app.run()