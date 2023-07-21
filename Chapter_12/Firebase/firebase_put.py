import urequests as requests
import ujson
# ผู้อ่านเปลี่ยน url ตามที่ Firebase กำหนด 
url = "https://esp32micropython-c827d.firebaseio.com/.json"
edit_date  = ujson.dumps({'-MdgJfrQdpUSWbGJ-JPt': {'humidity': 65, 'temperature': 35, 'time': '2021-07-02T19:16:00'}})
res = requests.put(url, headers = {'content-type': 'application/json'},  data = edit_date)
print(res.status_code)