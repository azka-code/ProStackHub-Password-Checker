import sqlite3
import os
from datetime import datetime

DATABASE = "data/password_events.db"

os.makedirs("data", exist_ok=True)


def init_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_event(event_type, severity, message):

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO events
        (timestamp, event_type, severity, message)
        VALUES (?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        event_type,
        severity,
        message
    ))

    connection.commit()
    connection.close()


def get_events():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT timestamp, event_type, severity, message
        FROM events
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows
