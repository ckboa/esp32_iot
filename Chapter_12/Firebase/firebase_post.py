import urequests as requests
import ujson
# ผู้อ่านเปลี่ยน url ตามที่ Firebase กำหนด 
url = "https://esp32micropython-c827d.firebaseio.com/.json"
current_time = '2021-07-02T19:16:00'
post_data = ujson.dumps({"time": current_time, "temperature": 30, "humidity": 75})
res = requests.post(url, headers = {'content-type': 'application/json'},  data = post_data)
print(res.status_code)