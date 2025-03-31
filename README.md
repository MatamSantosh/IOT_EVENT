1. MQTT Broker and Listener
Set up Mosquitto MQTT Broker
Create a Dockerfile for the Mosquitto MQTT broker:

2. Create Python-based MQTT Client
Install the gmqtt library:
pip install gmqtt


Create a Python script for the MQTT client:
import asyncio
import json
import logging
import sqlite3
from gmqtt import Client as MQTTClient

# Configure logging
logging.basicConfig(filename='mqtt_client.log', level=logging.INFO)

class MQTTListener:
    def __init__(self, broker_host):
        self.client = MQTTClient("mqtt_client")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker_host = broker_host
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Devices (
                device_id TEXT PRIMARY KEY,
                last_seen TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Events (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                sensor_type TEXT,
                sensor_value REAL,
                timestamp TEXT,
                FOREIGN KEY (device_id) REFERENCES Devices (device_id)
            )
        ''')
        conn.commit()
        conn.close()

    def on_connect(self, client, flags, rc, properties):
        logging.info("Connected to MQTT Broker")
        client.subscribe('/devices/events', qos=1)

    def on_message(self, client, topic, payload, qos, properties):
        message = json.loads(payload)
        if self.validate_message(message):
            self.store_message(message)
        else:
            logging.error(f"Invalid message: {message}")

    def validate_message(self, message):
        required_keys = {"device_id", "sensor_type", "sensor_value", "timestamp"}
        return required_keys.issubset(message.keys())

    def store_message(self, message):
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Devices (device_id, last_seen) VALUES (?, ?)
            ON CONFLICT(device_id) DO UPDATE SET last_seen=excluded.last_seen
        ''', (message['device_id'], message['timestamp']))
        cursor.execute('''
            INSERT INTO Events (device_id, sensor_type, sensor_value, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (message['device_id'], message['sensor_type'], message['sensor_value'], message['timestamp']))
        conn.commit()
        conn.close()

    async def connect(self):
        await self.client.connect(self.broker_host)

    async def run(self):
        await self.connect()
        await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    listener = MQTTListener('mqtt-broker')
    asyncio.run(listener.run())

Create a Dockerfile for the Client:
# Dockerfile for MQTT Client
FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "client.py"]


3. Real-Time Monitoring
Create a REST API using Flask:

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


Create a Dockerfile for the REST API:
# Dockerfile for Flask REST API
FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]


4. Data Storage
Extend the store_message method to store valid messages in an SQLite database:

import sqlite3

def store_message(self, message):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Devices (
            device_id TEXT PRIMARY KEY,
            last_seen TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            sensor_type TEXT,
            sensor_value REAL,
            timestamp TEXT,
            FOREIGN KEY (device_id) REFERENCES Devices (device_id)
        )
    ''')
    cursor.execute('''
        INSERT INTO Devices (device_id, last_seen) VALUES (?, ?)
        ON CONFLICT(device_id) DO UPDATE SET last_seen=excluded.last_seen
    ''', (message['device_id'], message['timestamp']))
    cursor.execute('''
        INSERT INTO Events (device_id, sensor_type, sensor_value, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (message['device_id'], message['sensor_type'], message['sensor_value'], message['timestamp']))
    conn.commit()
    conn.close()
	
	
5.  Dockerization
Create a docker-compose.yml file to orchestrate the setup:

version: '3'
services:
  mqtt-broker:
    build: ./mosquitto_broker
    ports:
      - "1883:1883"
  mqtt-client:
    build: ./mqtt_client
    depends_on:
      - mqtt-broker
  rest-api:
    build: ./rest_api
    ports:
      - "5000:5000"
    depends_on:
      - mqtt-client
	  
	  
6. Build and run the Docker containers:
Note: Run this command where the docker-compose.yml is located

docker-compose up --build


6. Testing and Documentation
Manually publish test messages using mosquitto_pub:

mosquitto_pub -h localhost -t /devices/events -m '{"device_id": "device1", "sensor_type": "temperature", "sensor_value": 23.5, "timestamp": "2025-03-28T12:00:00Z"}'



