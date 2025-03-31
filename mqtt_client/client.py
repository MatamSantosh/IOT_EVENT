import asyncio
import json
import logging
from gmqtt import Client as MQTTClient


logging.basicConfig(filename='mqtt_client.log', level=logging.INFO)

class MQTTListener:
    def __init__(self, broker_host):
        self.client = MQTTClient("mqtt_client")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker_host = broker_host

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
        pass

    async def connect(self):
        await self.client.connect(self.broker_host)

    async def run(self):
        await self.connect()
        await asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    listener = MQTTListener('mqtt-broker')
    asyncio.run(listener.run())
