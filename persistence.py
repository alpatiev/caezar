import sqlite3
import const

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
            self.__create_tables()
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

    def __create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {const.DB_TABLE_KEY_ID_LIST}
                              (id TEXT PRIMARY KEY);''')
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {const.DB_TABLE_KEY_USERS_LIST}
                              (id TEXT PRIMARY KEY,
                              {const.DB_ROW_KEY_USER_IMAGE_PATH} TEXT,
                              {const.DB_ROW_KEY_USER_PIPELINE} TEXT,
                              {const.DB_ROW_KEY_USER_PROMPT} TEXT);''')
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {const.DB_TABLE_KEY_LOGS_LIST}
                              ({const.DB_ROW_KEY_LOG_MESSAGE} TEXT);''')
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    # ----------------------------------------------
    # SECTION: Ids table
    # Table for key DB_TABLE_KEY_ID_LIST

    def fetch_all_ids(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT id FROM {const.DB_TABLE_KEY_ID_LIST}")
            result = cursor.fetchall()
            cursor.close()
            return [row[0] for row in result]
        except sqlite3.Error as e:
            return False, e

    def update_selected_id(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT OR IGNORE INTO {const.DB_TABLE_KEY_ID_LIST} (id) VALUES (?)", (id,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    def delete_selected_id(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {const.DB_TABLE_KEY_ID_LIST} WHERE id=?", (id,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    # ----------------------------------------------
    # SECTION: Users table
    # Table for key DB_TABLE_KEY_ID_LIST

    def fetch_selected_user(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {const.DB_TABLE_KEY_USERS_LIST} WHERE id=?", (id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except sqlite3.Error as e:
            return False, e

    def update_selected_user(self, item):
        try:
            table = const.DB_TABLE_KEY_USERS_LIST
            path = const.DB_ROW_KEY_USER_IMAGE_PATH
            pipe = const.DB_ROW_KEY_USER_PIPELINE
            prom = const.DB_ROW_KEY_USER_PROMPT
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT OR REPLACE INTO {table} (id, {path}, {pipe}, {prom}) VALUES (?, ?, ?, ?)",
                           (item.id, item.image_path, item.pipeline, item.prompt))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e
    
    def delete_selected_user(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {const.DB_TABLE_KEY_USERS_LIST} WHERE id=?", (id,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    # ----------------------------------------------
    # SECTION: Logs table
    # Table for key DB_TABLE_KEY_LOGS_LIST

    def fetch_all_logs(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT {const.DB_ROW_KEY_LOG_MESSAGE} FROM {const.DB_TABLE_KEY_LOGS_LIST}")
            result = cursor.fetchall()
            cursor.close()
            return [row[0] for row in result]
        except sqlite3.Error as e:
            return False, e

    def delete_all_logs(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {const.DB_TABLE_KEY_LOGS_LIST}")
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    def update_selected_log(self, text):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {const.DB_TABLE_KEY_LOGS_LIST} ({const.DB_ROW_KEY_LOG_MESSAGE}) VALUES (?)", (text,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e
