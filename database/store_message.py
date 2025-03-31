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
