import urequests as requests
import ujson
# ผู้อ่านเปลี่ยน url ตามที่ Firebase กำหนด 
url = "https://esp32micropython-c827d.firebaseio.com/-MdgJfrQdpUSWbGJ-JPt/.json"
res = requests.delete(url, headers = {'content-type': 'application/json'})
print(res.status_code)