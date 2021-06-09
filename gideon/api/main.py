from flask import Flask, jsonify, request
import db_queries

app = Flask(__name__)
app.config['DEBUG'] = True

@app.errorhandler(404)
def http_not_found(e):
    return jsonify({"status": 404})

@app.route('/api/v1/', methods=['GET'])
def root():
    return jsonify({"status": 200})


@app.route('/api/v1/insert_new_user/', methods=['GET'])
def insert_new_user():

    fname = request.args.get('fname')
    sname = request.args.get('sname')
    email = request.args.get('email')
    password = request.args.get('pass')
    
    if fname and sname and email and password:
        try:
            conn = db_queries.get_conn()
            db_queries.insert_user(conn, (fname, sname, email, password))
            return jsonify({"message": "success"})
        except:
            return jsonify({"message": "error"})
    else:
        return jsonify({"message": "invalid data"})

@app.route('/api/v1/insert_new_event/', methods=['GET'])
def insert_new_event():

    user_id = request.args.get('user_id')
    event_title = request.args.get('title')
    event_desc = request.args.get('desc')
    event_datetime = request.args.get('datetime')
    event_tags = request.args.get('tags')
    event_lat = request.args.get('lat')
    event_lon = request.args.get('lon')
    
    if not event_tags:
            event_tags = 'null'
    
    if user_id and event_title and event_desc and event_datetime and event_tags and event_lat and event_lon:
        try:
            conn = db_queries.get_conn()
            result = db_queries.insert_event(conn, (int(user_id), event_title, event_desc, event_datetime, event_tags, float(event_lat), float(event_lon)))
            if result:
                return jsonify({"message": "success"})
            else:
                return jsonify({"message": "no user with this id found"})
        except:
            return jsonify({"message": "error"})
    else:
        return jsonify({"message": "invalid data"})
        

@app.route('/api/v1/get_user_info', methods=['GET'])
def get_user_info():
    
    user_id = request.args.get('user_id')
  
    if user_id:
        try:
            conn = db_queries.get_conn()
            data = db_queries.get_user_data(conn, user_id)
            if not data:
                return jsonify({"message": "no user with this id found"})
            
            return jsonify({"status":200, "data":{"user_id": data[0][0], "fname": data[0][1], "sname": data[0][2], "email": data[0][3], "password": data[0][4]}})
        except:
            return jsonify({"message":"error"})
    else:
        return jsonify({"message": "invalid data"})


@app.route('/api/v1/get_user_events/', methods=['GET'])
def get_user_events():
    
    user_id = request.args.get('user_id')
    
    if user_id:
        try:
            conn = db_queries.get_conn()
            data = db_queries.get_user_events(conn, user_id)
            
            if not data:
                return jsonify({"message": "no user with this id found"})
                
            return_str = []
            for i in data:
                return_str.append({"event_id": i[0], "event_title": i[2], "event_desc": i[3], "event_datetime": i[4], "event_tags": i[5], "event_lat": i[6], "event_lon": i[7]})
            return_str.append({"status": 200, "user_id": data[0][1]})
            
            return jsonify(return_str)
        except:
            return jsonify({"message": "error"})
    else:
        return jsonify({"message": "invalid data"})


@app.route('/api/v1/test/', methods=['GET'])
def test():
    db = db_queries.get_db_path()
    return jsonify({"message": db})
    

app.run()