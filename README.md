1. **MQTT Broker and Listener**:
Set up Mosquitto MQTT Broker,
Create a Dockerfile for the Mosquitto MQTT broker:

2. **Create Python-based MQTT Client**:
Create a Dockerfile for the Client:

3. **Real-Time Monitoring**:
Create a REST API using Flask:
Create a Dockerfile for the REST API:

4. **Data Storage**:
Extend the store_message method to store valid messages in an SQLite database:
		
5.  **Dockerization**:
Create a docker-compose.yml file to orchestrate the setup:


**Detailed Setup Instructions**:

**Clone the repository**:
   ```bash
   git clone https://github.com/MatamSantosh/IOT_EVENT.git
   cd IOT_EVENT
   ```
	  
**Build and run the Docker containers**:
Note: Run this command where the docker-compose.yml is located
 ```bash
docker-compose up --build
 ```

#### System Architecture Overview
```markdown
## System Architecture Overview

The system consists of the following components:
- **Mosquitto MQTT Broker**: Handles MQTT messaging.
- **Python MQTT Client**: Listens to MQTT messages, validates, and stores them.
- **SQLite Database**: Stores device and event data.
- **Flask REST API**: Provides endpoints for real-time monitoring.
- **Docker Compose**: Manages container orchestration.
```

### API Documentation

### List All Devices
- **Endpoint**: `GET /devices`
- **Description**: Retrieves a list of all registered devices and their last active timestamps.

### Retrieve Events for a Device
- **Endpoint**: `GET /events/<device_id>`
- **Description**: Retrieves the latest events for a given device.
- **Parameters**:
  - `device_id` (string): The ID of the device.



**Testing and Documentation**:
Manually publish test messages using mosquitto_pub:
Test Case 1: Valid Message
 Publish a valid message:
   
   ```bash
   mosquitto_pub -h localhost -t /devices/events -m '{"device_id": "device1", "sensor_type": "temperature", "sensor_value": 23.5, "timestamp": "2025-03-28T12:00:00Z"}'
   ```
Test Case 2: Invalid Message
 Publish an invalid message:

   ```bash
   mosquitto_pub -h localhost -t /devices/events -m '{"device_id": "device1", "sensor_type": "temperature"}'

   ```


6. **Access the REST API**: at 'http://localhost:5000/devices'



