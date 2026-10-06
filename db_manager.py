import sqlite3
from datetime import datetime

DB_NAME = "daily_science.db"

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.create_tables()
        self.seed_data()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fact TEXT,
                explanation TEXT,
                category TEXT,
                nda_note TEXT,
                sub_category TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                setup_completed INTEGER DEFAULT 0,
                notification_time TEXT DEFAULT '07:00',
                streak INTEGER DEFAULT 0,
                last_active_date TEXT
            )
        ''')
        cursor.execute("INSERT OR IGNORE INTO user_profile (id) VALUES (1)")
        self.conn.commit()

    def seed_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM facts")
        if cursor.fetchone()[0] == 0:
            facts = [
                ("Light travels faster than sound.", "This is why you see lightning before hearing thunder.", "Physics", "Crucial for optic concepts.", "Optics"),
                ("Water boils at 100°C at sea level.", "Atmospheric pressure affects boiling point.", "Chemistry", "Important for NDA thermodynamics.", "Physical Chemistry"),
                ("Mitochondria is the powerhouse of the cell.", "It generates ATP for cellular functions.", "Biology", "Frequently asked in General Science.", "Cell Biology")
            ]
            cursor.executemany("INSERT INTO facts (fact, explanation, category, nda_note, sub_category) VALUES (?, ?, ?, ?, ?)", facts)
            self.conn.commit()

    def get_user_data(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT notification_time, setup_completed, streak, last_active_date FROM user_profile WHERE id = 1")
        return cursor.fetchone()

    def update_setup(self, notification_time):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE user_profile SET notification_time = ?, setup_completed = 1 WHERE id = 1", (notification_time,))
        self.conn.commit()

    def update_streak(self):
        cursor = self.conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        data = self.get_user_data()
        last_date = data[3]
        streak = data[2]

        if last_date != today:
            streak += 1
            cursor.execute("UPDATE user_profile SET streak = ?, last_active_date = ? WHERE id = 1", (streak, today))
            self.conn.commit()
        return streak

    def get_daily_fact(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM facts ORDER BY RANDOM() LIMIT 1")
        return cursor.fetchone()

    def close(self):
        self.conn.close()
