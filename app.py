import sys
from bot import BotModule
from logs import LogModule
from replies import PromptModule
from persistence import StorageModule

# python app.py 6368855906:AAFChqeoftuth2Y7LsOhkpgOSMMoD7yoD2o ps4jYK4gv0Accq3o

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    bot_token = sys.argv[1]
    admin_key = sys.argv[2]

    storage_module = StorageModule()
    prompt_module = PromptModule()
    log_module = LogModule()
    bot_module = BotModule(bot_token, admin_key, storage_module, prompt_module, log_module)
    bot_module.start()
