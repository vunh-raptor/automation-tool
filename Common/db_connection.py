import sqlite3
from time import time as time


class DBConnection:
    # db_path = "\\\\vn-vwl5050\\group2\\SD_Storage\\AutomationHubDB\\automation_hub.db"
    
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def create_table_schema(self):
        self.cursor.execute("CREATE TABLE log(test_value)")
        self.connection.commit()

    def insert_log(self, test_value):
        # timestamp = time()
        self.cursor.execute('''
        INSERT INTO log (test_value) VALUES (?)
        ''', (test_value,))
        self.connection.commit()

    def execute_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        
    def fetch_data_from_db(self, query):
        data = self.cursor.execute(query).fetchall()
        return data
        

    def close(self):
        self.connection.close()
        
        