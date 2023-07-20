from flask_mysqldb import MySQL
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__, template_folder="www/")
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'test'
app.config['MYSQL_DB'] = 'esp_data'
mysql = MySQL(app)

@app.route('/sensor_dth', methods=['POST'])
def add_dht():
    try:  
        data = request.get_json() 
        print(data)
        global temperature, humidity
        temperature = data['temperature']
        humidity = data['humidity']
        current_time = datetime.now()
        date_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(date_time)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO sensor_dht (temperature, humidity, date_time) VALUES (%s, %s, %s)", (temperature, humidity, date_time))
        mysql.connection.commit()
        cur.close()

        resp = jsonify(message="Data added successfully!")
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        return jsonify(message="adding data error"), 500

@app.route('/get_data')
def get_data():
    data = {'temperature': temperature, 
            'humidity': humidity}
    return jsonify(data)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=5000, ssl_context='adhoc' )
