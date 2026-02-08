import sqlite3
from datetime import datetime

DB_NAME = "attendance.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Table users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    # Table attendance
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            confidence REAL,
            UNIQUE(user_id, date),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()

def add_user(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (name, created_at)
        VALUES (?, ?)
    """, (name, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def user_exists(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()

    conn.close()
    return result is not None


def attendance_exists(user_id, date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id FROM attendance
        WHERE user_id = ? AND date = ?
    """, (user_id, date))

    result = cursor.fetchone()
    conn.close()
    return result is not None


def add_attendance(user_id, confidence):
    today = datetime.now().date().isoformat()
    time_now = datetime.now().time().strftime("%H:%M:%S")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO attendance (user_id, date, time, confidence)
            VALUES (?, ?, ?, ?)
        """, (user_id, today, time_now, confidence))

        conn.commit()
        success = True

    except sqlite3.IntegrityError:
        # Violation de la contrainte UNIQUE(user_id, date)
        success = False

    conn.close()
    return success
