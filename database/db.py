import sqlite3
import os

DB_PATH = os.path.join("data", "agenda.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn