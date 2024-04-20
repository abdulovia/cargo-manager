# database.py
import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS transports (
                            vehicle_id TEXT PRIMARY KEY,
                            capacity REAL,
                            is_booked INTEGER,
                            model TEXT,
                            manufacturer TEXT)''')
        self.conn.commit()

    def add_transport(self, vehicle_id, capacity, is_booked=0, model=None, manufacturer=None):
        self.cur.execute("INSERT INTO transports VALUES (?, ?, ?, ?, ?)", (vehicle_id, capacity, is_booked, model, manufacturer))
        self.conn.commit()

    def remove_transport(self, vehicle_id):
        self.cur.execute("DELETE FROM transports WHERE vehicle_id=?", (vehicle_id,))
        self.conn.commit()

    def get_all_transports(self):
        self.cur.execute("SELECT * FROM transports")
        return self.cur.fetchall()

    def get_available_transports(self):
        self.cur.execute("SELECT * FROM transports WHERE is_booked=0")
        return self.cur.fetchall()

    def get_booked_transports(self):
        self.cur.execute("SELECT * FROM transports WHERE is_booked=1")
        return self.cur.fetchall()

    def close_connection(self):
        self.conn.close()
