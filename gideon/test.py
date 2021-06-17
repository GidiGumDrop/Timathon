import requests

res = requests.post('http://127.0.0.1:5000/api/insert_new_event/', json={'user_id':5, 'title':'test', 'desc':'test', 'datetime':'test', 'tags':'test,test2', 'lat':45, 'lon':45, 'agegroup':'0-80', 'max_ppl':5, 'imgs':'test.png'})
res = requests.post('http://127.0.0.1:5000/api/insert_user_attendance/', json={'user_id':6, 'event_id':12})
print(res.text)

#update user info
# {'user_id':1, 'fname':'gidi', 'sname':'weiss', 'dob':'2004-10-04', 'email':'test', 'password':'test', 'user_pfp':'pic.jpg'}

#update event info
#{'event_id':2, 'user_id':2, 'title':'test', 'desc':'test', 'datetime':'test', 'tags':'test,test2', 'lat':45, 'lon':45, 'agegroup':'0-80', 'imgs':'test.png'}