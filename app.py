import sys
import constants
from bot import BotModule
from logs import LogModule
from replies import PromptModule
from persistence import StorageModule

# python app.py 6368855906:AAFChqeoftuth2Y7LsOhkpgOSMMoD7yoD2o ps4jYK4gv0Accq3o

# --------------------------------------------------
# NOTE: Entry point
# Expects two arguments <bot_token> and <auth_key>:
#   bot_token - specific telefram bot token
#   auth_key - authorization key, protects fraudulent users 
# All users and logs stored in database.sqlite
#
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    bot_token = sys.argv[1]
    auth_key = sys.argv[2]

    storage_module = StorageModule(constants.PATH_DATABASE)
    prompt_module = PromptModule()
    log_module = LogModule()
    bot_module = BotModule(bot_token, auth_key, storage_module, prompt_module, log_module)
    bot_module.start()
