import sqlite3
import CONSTANTS

# --------------------------------------------------
# NOTE: Storage module
# Main storage class for SQL operations
#
class StorageModule:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    # ----------------------------------------------
    # SECTION: Storage lifecycle

    def connect_database(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.create_table()
            return True
        except sqlite3.Error as e:
            return False, 

    def disconnect_database(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            return True
        else:
            return False, "no database connection to disconnect"

    # ----------------------------------------------
    # SECTION: CRUD methods

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS data
                              (key TEXT PRIMARY KEY,
                              value TEXT);''')
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    def save_value(self, key, value):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO data (key, value) VALUES (?, ?)", (key, value))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    def get_value(self, key):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT value FROM data WHERE key=?", (key,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]
            else:
                return False, f"no value found for key {key}"
        except sqlite3.Error as e:
            return False, e

    def delete_value(self, key):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM data WHERE key=?", (key,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e
