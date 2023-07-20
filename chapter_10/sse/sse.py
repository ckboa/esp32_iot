from microWebSrv import MicroWebSrv
import esp32


def _httpHandlerTestGet(httpClient, httpResponse) :
    with open('www/index.html', 'r') as file:
        content = file.read()
    httpResponse.WriteResponseOk(headers=None,
                                 contentType="text/html",
                                 contentCharset="UTF-8",
                                 content=content)

# ฟังก์ชันสำหรับจัดการกับ POST request
def _httpHandlerTestPost(httpClient, httpResponse):
    # รับข้อมูลจากฟอร์มที่ส่งมา
    formData = httpClient.ReadRequestPostedFormData()
    firstname = formData['username']
    print('Login by: {}'.format(firstname)) 
    
    content = open('www/result.html', 'r').read()
    content = content.replace('{firstname}', firstname)
    
    # ส่ง response กลับไปยัง client
    httpResponse.WriteResponseOk(headers=None, contentType="text/html", contentCharset="UTF-8", content=content)
    

count = 0 
def _httpHandlerSensorGet(httpClient, httpResponse):
    try:
        temp, hall = (esp32.raw_temperature() - 32.0) / 1.8, esp32.hall_sensor()
        global count 
        count = count + 1
        data = '{2}: Temp: {0:.2f} C; Hall: {1:.2f}'.format(temp, hall, count)
    except:
        data = 'Attempting to read sensor...'
    
    httpResponse.WriteResponseOk(
        headers = ({'Cache-Control': 'no-cache', 'Access-Control-Allow-Origin': '*'}),
        contentType = 'text/event-stream',
        contentCharset = 'UTF-8',
        content = 'data: {0}\n\n'.format(data)
    )
# สร้าง route handler และกำหนดเพื่อใช้งาน
routeHandlers = [
    ( "/index", "GET", _httpHandlerTestGet ),
    ( '/test', 'POST', _httpHandlerTestPost ),
    ( "/sensor", "GET", _httpHandlerSensorGet )
]

print("Server-Sent Started") 
srv = MicroWebSrv(routeHandlers = routeHandlers, webPath='www/')
srv.Start(threaded = False)
