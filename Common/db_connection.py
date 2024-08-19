import sqlite3
from time import time as time


class DBConnection:
    db_path = "\\\\vn-vwl5050\\group2\\SD_Storage\\AutomationHubDB\\log.db"
    
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def create_table_schema(self):
        self.cursor.execute("CREATE TABLE log(timestamp, hrcode, message, status, account)")
        self.connection.commit()

    def insert_log(self, hrcode, message, status, account):
        timestamp = time()
        self.cursor.execute(f"INSERT INTO log VALUES({timestamp}, {hrcode}, {message}, {status}, {account})")
        self.connection.commit()

    def read_log(self, table_name):
        self.cursor.execute("SELECT * from log")       

    def close(self):
        self.connection.close()
        
        