1. MQTT Broker and Listener:
Set up Mosquitto MQTT Broker,
Create a Dockerfile for the Mosquitto MQTT broker:


2. Create Python-based MQTT Client:
Create a Dockerfile for the Client:


3. Real-Time Monitoring
Create a REST API using Flask:
Create a Dockerfile for the REST API:


4. Data Storage
Extend the store_message method to store valid messages in an SQLite database:
	
	
5.  Dockerization
Create a docker-compose.yml file to orchestrate the setup:
	  
	  
6. Build and run the Docker containers:
Note: Run this command where the docker-compose.yml is located

docker-compose up --build


6. Testing and Documentation
Manually publish test messages using mosquitto_pub:

mosquitto_pub -h localhost -t /devices/events -m '{"device_id": "device1", "sensor_type": "temperature", "sensor_value": 23.5, "timestamp": "2025-03-28T12:00:00Z"}'


7.  Access the REST API at 'http://localhost:5000/devices'



