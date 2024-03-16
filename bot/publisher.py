import os
import json
import threading
import time
from module import BotModule

# --------------------------------------------------
# ENTITY: STORAGE
# Main storage class for SQL operations

class PublisherModule(BotModule):

    # ----------------------------------------------
    # SECTION: LIFECYCLE

    def __init__(self):
        self.target_path = target_path
        self.message_queue_callback = None
        self.running = False
        self.thread = None
        self.last_modified = None

    def start(self, config, message_queue_callback):
        if not os.path.exists(self.target_path):
            self.create_initial_file()
        self.running = True
        self.message_queue_callback = message_queue_callback
        self.thread = threading.Thread(target=self.watch_file)
        self.thread.start()

    # ----------------------------------------------
    # SECTION: SETUPS

    def create_initial_file(self):
        initial_data = {"message_queue": []}
        with open(self.target_path, 'w') as file:
            json.dump(initial_data, file, indent=4)

    # ----------------------------------------------
    # SECTION: OBSERVING

    def watch_file(self):
        while self.running:
            time.sleep(const.TIME_S_WATCH_THROTTLE)
            if os.path.exists(self.target_path):
                last_change = os.path.getmtime(self.target_path)
                if last_change != self.last_modified:
                    self.last_modified = last_change
                    self.check_file()

    def check_file(self):
        if os.path.exists(self.target_path):
            with open(self.target_path, 'r') as file:
                data = json.load(file)
                message_queue = data.get('message_queue', [])
                if message_queue:
                    for message in message_queue:
                        if self.message_queue_callback:
                            self.message_queue_callback(message)
                    data['message_queue'] = []
                    self.write_data(data)

    def write_data(self, data):
        with open(self.target_path, 'w') as file:
            json.dump(data, file, indent=4)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
