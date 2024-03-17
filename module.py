import abc

# --------------------------------------------------
# ENTITY: BOT MODULE
# Abstract class for all bot services,
# helps to ensure base functionality.

class BotModule(abc.ABC):

    @abc.abstractmethod
    def start(self, config):
        pass

    @abc.abstractmethod
    def stop(self):
        pass