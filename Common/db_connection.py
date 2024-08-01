import sqlite3
from time import time as time


class DBConnection:
    db_path = "\\\\vn-vwl5050\\group2\\SD_Storage\\AutomationHubDB\\log.db"
    
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def create_table_schema(self):
        self.cursor.execute("CREATE TABLE log(timestamp, id, message, status)")
        self.connection.commit()

    def insert_log(self, id, message, status):
        timestamp = time()
        self.cursor.execute(f"INSERT INTO log VALUES({timestamp}, {id}, {message}, {status})")
        self.connection.commit()

    def close(self):
        self.connection.close()
        
        