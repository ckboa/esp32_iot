import urequests as requests
import ujson
# ผู้อ่านเปลี่ยน url ตามที่ Firebase กำหนด 
url = "https://esp32micropython-c827d.firebaseio.com/.json"
response = requests.get(url)
print(response.text)