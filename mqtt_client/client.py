import asyncio
import json
import logging
import sqlite3
from gmqtt import Client as MQTTClient

# Configure logging
logging.basicConfig(filename='mqtt_client.log', level=logging.INFO)

class MQTTListener:
    def __init__(self, broker_host, broker_port=1883):
        self.client = MQTTClient("mqtt_client")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.setup_database()

    def setup_database(self):
        conn = sqlite3.connect('iot_events.db')
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
        conn = sqlite3.connect('iot_events.db')
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
        await self.client.connect(self.broker_host, self.broker_port)

    async def run(self):
        await self.connect()
        await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    listener = MQTTListener('mqtt-broker')
    asyncio.run(listener.run())
