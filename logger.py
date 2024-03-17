from module import BotModule

# --------------------------------------------------
# ENTITY: LOGGER
# Main logger class for writing log to disk,
# also printing debug info if enabled.

class LoggerModule(BotModule):

    # ----------------------------------------------
    # SECTION: LIFECYCLE

    def __init__(self):
        pass

    def start(self, config):
        pass

    def stop(self):
        pass

    # ----------------------------------------------
    # SECTION: DISPATCH

    def log_info(self, message):
        print("⚪️ " + message)

    def log_event(self, message):
        print("🟢 " + message)

    def log_error(self, message):
        print("🔴 " + message)

    # ----------------------------------------------
    # SECTION: INFO LEVEL

    def info_app_launched(self):
        self.log_info("application launched")

    def info_unrecognized_chat_attempt(self, chat_id, command):
        self.log_info(f"rejected {command} from chat {chat_id}")

    # ----------------------------------------------
    # SECTION: EVENTS LEVEL

    def event_sent_notification(self):
        self.log_event("sent notification")

    # ----------------------------------------------
    # SECTION: ERROR LEVEL

    def error_app_launch(self):
        self.log_error("application launch")

    def error_sending_notification(self):
        self.log_error("sending notification")

