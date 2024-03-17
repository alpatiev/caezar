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
    # SECTION: DEBUG

    def __debug_print_daemon(self):
        s = 10
        for _ in range(10):
            with open("stream.txt", 'w') as file:
                file.write(f"running for {s} seconds..")
            s += 1
            time.sleep(1)
