import os
import json
import threading
import const
import time

class QueueObserver:
    def __init__(self, target_path, callback):
        self.target_path = target_path
        self.callback = callback
        self.running = False
        self.thread = None
        self.last_modified = None

    def start(self):
        if not os.path.exists(self.target_path):
            self.create_initial_file()

        self.running = True
        self.thread = threading.Thread(target=self.watch_file)
        self.thread.start()

    def create_initial_file(self):
        initial_data = {"message_queue": []}
        with open(self.target_path, 'w') as file:
            json.dump(initial_data, file, indent=4)

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
                        time.sleep(const.TIME_S_MSG_THROTTLE)
                        if self.callback:
                            self.callback(message)
                    data['message_queue'] = []
                    self.write_data(data)

    def write_data(self, data):
        with open(self.target_path, 'w') as file:
            json.dump(data, file, indent=4)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
