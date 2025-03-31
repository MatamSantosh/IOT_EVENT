from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/devices', methods=['GET'])
def get_devices():
    conn = sqlite3.connect('../database/events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Devices')
    devices = cursor.fetchall()
    conn.close()
    return jsonify(devices)

@app.route('/events/<device_id>', methods=['GET'])
def get_events(device_id):
    conn = sqlite3.connect('../database/events.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Events WHERE device_id=?', (device_id,))
    events = cursor.fetchall()
    conn.close()
    return jsonify(events)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
