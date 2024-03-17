import os
import json
import threading
import time
from module import BotModule

# --------------------------------------------------
# ENTITY: PUBLISHER
# Main observer class for updates from buffer.json

class PublisherModule(BotModule):

    # ----------------------------------------------
    # SECTION: LIFECYCLE

    def __init__(self):
        self.running = False
        self.target_path = None
        self.message_queue_callback = None
        self.thread = None
        self.last_modified = None
        self.SEC_INTERVAL = None
        self.SEC_THROTTLE = None
        self.MESSAGE_QUEUE_KEY = "message_queue"

    def start(self, config, message_queue_callback):
        self.__configure(config)
        if not os.path.exists(self.target_path):
            self.__create_default_file()
        self.running = True
        self.message_queue_callback = message_queue_callback
        self.thread = threading.Thread(target=self.watch_file)
        self.thread.start()

    # ----------------------------------------------
    # SECTION: SETUPS

    def __configure(self, config):
        self.target_path = config.get("resources_path", {}).get("buffer", None)
        self.SEC_INTERVAL = config.get("bot_threading", {}).get("observing_interval", None)
        self.SEC_THROTTLE = config.get("bot_threading", {}).get("throttling_time", None)

    def __create_default_file(self):
        initial_data = {self.MESSAGE_QUEUE_KEY: []}
        with open(self.target_path, 'w') as file:
            json.dump(initial_data, file, indent=4)

    # ----------------------------------------------
    # SECTION: OBSERVING

    def watch_file(self):
        while self.running:
            time.sleep(self.SEC_INTERVAL)
            if os.path.exists(self.target_path):
                last_change = os.path.getmtime(self.target_path)
                if last_change != self.last_modified:
                    self.last_modified = last_change
                    self.check_file()

    def check_file(self):
        if os.path.exists(self.target_path):
            with open(self.target_path, 'r') as file:
                data = json.load(file)
                message_queue = data.get(self.MESSAGE_QUEUE_KEY, [])
                if message_queue:
                    for message in message_queue:
                        if self.message_queue_callback:
                            time.sleep(self.SEC_THROTTLE)
                            self.message_queue_callback(message)
                    data[self.MESSAGE_QUEUE_KEY] = []
                    self.write_data(data)

    def write_data(self, data):
        with open(self.target_path, 'w') as file:
            json.dump(data, file, indent=4)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
