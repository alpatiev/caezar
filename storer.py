import sqlite3
from module import BotModule

# --------------------------------------------------
# ENTITY: STORAGE
# Main storage class for SQL operations

class StorageModule(BotModule):

    # ----------------------------------------------
    # SECTION: LIFECYCLE

    def __init__(self):
        pass

    def start(self, config):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.__create_tables()
        except sqlite3.Error as e:
            return False, 

    def stop(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            return True
        else:
            return False, "no database connection to disconnect"

    # ----------------------------------------------
    # SECTION: SETUPS
    
    def __configure(self, config):
        pass

    def __create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.TK_USR_LIST}
                              (id TEXT PRIMARY KEY,
                              {self.RK_USR_DIR} TEXT,
                              {self.RK_USR_INFO_MSG} TEXT);''')
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.TK_LOG_LIST}
                              ({self.RK_LOG_ITEM} TEXT);''')
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
            cursor.execute(f"SELECT id FROM {self.DB_TABLE_KEY_ID_LIST}")
            result = cursor.fetchall()
            cursor.close()
            return [row[0] for row in result]
        except sqlite3.Error as e:
            return False, e

    def update_selected_id(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT OR IGNORE INTO {self.DB_TABLE_KEY_ID_LIST} (id) VALUES (?)", (id,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    def delete_selected_id(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {self.DB_TABLE_KEY_ID_LIST} WHERE id=?", (id,))
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
            cursor.execute(f"SELECT * FROM {self.DB_TABLE_KEY_USERS_LIST} WHERE id=?", (id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except sqlite3.Error as e:
            return False, e

    def update_selected_user(self, item):
        try:
            table = self.DB_TABLE_KEY_USERS_LIST
            path = self.DB_ROW_KEY_USER_IMAGE_PATH
            pipe = self.DB_ROW_KEY_USER_PIPELINE
            prom = self.DB_ROW_KEY_USER_PROMPT
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
            cursor.execute(f"DELETE FROM {self.DB_TABLE_KEY_USERS_LIST} WHERE id=?", (id,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    # ----------------------------------------------
    # SECTION: LOGS
    # Table for key DB_TABLE_KEY_LOGS_LIST

    def fetch_all_logs(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT {self.DB_ROW_KEY_LOG_MESSAGE} FROM {self.DB_TABLE_KEY_LOGS_LIST}")
            result = cursor.fetchall()
            cursor.close()
            return [row[0] for row in result]
        except sqlite3.Error as e:
            return False, e

    def delete_all_logs(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {self.DB_TABLE_KEY_LOGS_LIST}")
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    def update_selected_log(self, text):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {self.DB_TABLE_KEY_LOGS_LIST} ({self.DB_ROW_KEY_LOG_MESSAGE}) VALUES (?)", (text,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e
