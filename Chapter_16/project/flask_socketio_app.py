from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_mqtt import Mqtt
from flask_mysqldb import MySQL
from datetime import datetime
import json


app = Flask(__name__, template_folder="www/")
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)
mqtt = Mqtt(app)

app.config['MQTT_BROKER_URL'] = 'localhost'  
app.config['MQTT_BROKER_PORT'] = 1883  
app.config['MQTT_USERNAME'] = ''  
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 300 
app.config['MQTT_TLS_ENABLED'] = False 

#mqtt_broker = "localhost"
mqtt_sensor_topic = "sensor_data"
mqtt_relay_topic = "relay_controller"

#MySQL Configure
mysql = MySQL(app)
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'esp_data'


def parse_sensor_data(data):
    sensor_data = json.loads(data)
    temperature = sensor_data.get('temperature', 0)
    humidity = sensor_data.get('humidity', 0)
    esp32_temperature = sensor_data.get('esp32Temperature', 0)

    #Send to Database
    with app.app_context():
        send_db(temperature, humidity, esp32_temperature)

    return {
        'temperature': temperature,
        'humidity': humidity,
        'esp32Temperature': esp32_temperature
    }

# MySQL
def send_db(temperature, humidity, esp32_temperature):
    try:
        current_time = datetime.now()
        date_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sensor_data(temperature, humidity, esp32_temperature, update_time) VALUES (%s, %s, %s, %s)",
                        (temperature, humidity, esp32_temperature, date_time))
        mysql.connection.commit()
        print("Insert data")
        cur.close()

    except Exception as e:
        print(e)
        return "error"

# MQTT
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(mqtt_sensor_topic)
    print("Connected to MQTT Broker")

@mqtt.on_message()
def handle_message(client, userdata, message):
    data = message.payload.decode()
    print("Received message:", data)
    
    #Send to WebBrowser
    if message.topic == mqtt_sensor_topic:
        socketio.emit('sensorData', parse_sensor_data(data), namespace='/')

#Socket.IO
@socketio.on('relay')
def handle_relay(data):
    print("Received message:", data)
    #Send to Broker
    mqtt.publish(mqtt_relay_topic, json.dumps(data))

    #Send to Database
    with app.app_context():
        relay_number = data.get('relayNumber', 0)
        relay_state = data.get('state', 0)
        try:
            current_time = datetime.now()
            date_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO relay_data (relay_number, relay_state, update_time) VALUES (%s, %s, %s)", 
                        (relay_number, relay_state, date_time))
            mysql.connection.commit()
            cur.close()

            resp = jsonify(message="Data added successfully!!")
            resp.status_code = 200
            return print(resp)
        except Exception as e:
            print(e)
            return jsonify(message="adding data error"), 500

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    socketio.emit('message', 'Connected to server')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    socketio.emit('message', 'state: disconnected')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
