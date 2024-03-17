import sqlite3
from module import BotModule

# --------------------------------------------------
# ENTITY: STORAGE
# Main storage class for SQL operations

class StorageModule(BotModule):

    # ----------------------------------------------
    # SECTION: LIFECYCLE

    def __init__(self):
        self.db_path = None
        self.TK_CHAT_LIST = None
        self.RK_CHAT_DIR = None
        self.RK_CHAT_MSG = None
        self.TK_LOG_LIST = None
        self.RK_LOG_ITEM = None

    def start(self, config):
        try:
            self.__configure(config)
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
        self.db_path = config.get("resources_path", {}).get("database", None)
        chats = config.get("database", {}).get("chat_list_table", {})
        logs = config.get("database", {}).get("logs_list_table", {})
        self.TK_CHAT_LIST = chats.get("key", None)
        self.RK_CHAT_DIR = chats.get("row_keys", {}).get("media_dir", None)
        self.RK_CHAT_MSG = chats.get("row_keys", {}).get("info_message", None)
        self.TK_LOG_LIST = logs.get("key", None)
        self.RK_LOG_ITEM = logs.get("row_keys", {}).get("event", None)
        print(self.TK_CHAT_LIST, self.RK_CHAT_DIR, self.RK_CHAT_MSG, self.TK_LOG_LIST, self.RK_LOG_ITEM )


    def __create_tables(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.TK_CHAT_LIST}
                              (id TEXT PRIMARY KEY,
                              {self.RK_CHAT_DIR} TEXT,
                              {self.RK_CHAT_MSG} TEXT);''')
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.TK_LOG_LIST}
                              ({self.RK_LOG_ITEM} TEXT);''')
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    # ----------------------------------------------
    # SECTION: CHATS
    # Table for key TK_CHAT_LIST

    def chat_fetch_all_ids(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT id FROM {self.TK_CHAT_LIST}")
            result = cursor.fetchall()
            cursor.close()
            return [row[0] for row in result]
        except sqlite3.Error as e:
            return False, e

    def chat_fetch_selected(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM {self.TK_CHAT_LIST} WHERE id=?", (id,))
            result = cursor.fetchone()
            cursor.close()
            return result
        except sqlite3.Error as e:
            return False, e

    def chat_update_selected(self, item):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT OR REPLACE INTO {self.TK_CHAT_LIST} (id, {self.RK_CHAT_DIR}, {self.RK_CHAT_MSG}) VALUES (?, ?, ?)",
                           (item.id, item.image_path, item.pipeline, item.prompt))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e
    
    def chat_delete_selected(self, id):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {self.TK_CHAT_LIST} WHERE id=?", (id,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    # ----------------------------------------------
    # SECTION: LOGS
    # Table for key TK_LOG_LIST

    def log_fetch_all(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT {self.RK_LOG_ITEM} FROM {self.TK_LOG_LIST}")
            result = cursor.fetchall()
            cursor.close()
            return [row[0] for row in result]
        except sqlite3.Error as e:
            return False, e

    def log_delete_all(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM {self.TK_LOG_LIST}")
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e

    def log_create_item(self, message):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO {self.TK_LOG_LIST} ({self.RK_LOG_ITEM}) VALUES (?)", (message,))
            self.conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            return False, e
