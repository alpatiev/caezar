import sys
import constants
from bot import BotModule
from logs import LogModule
from replies import PromptModule
from persistence import StorageModule

# TOKEN 6368855906:AAFChqeoftuth2Y7LsOhkpgOSMMoD7yoD2o
# CHAT_ID 983280553
# python app.py 6368855906:AAFChqeoftuth2Y7LsOhkpgOSMMoD7yoD2o 983280553

# --------------------------------------------------
# NOTE: Entry point
# Expects two arguments <bot_token> and <chat_id>:
#   bot_token - specific telefram bot token
#   auth_key - authorization key, protects fraudulent users 
# All users and logs stored in database.sqlite
#
if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(1)
    bot_token = sys.argv[1]
    chat_id = sys.argv[2]

    storage_module = StorageModule(constants.PATH_DATABASE)
    prompt_module = PromptModule()
    log_module = LogModule()
    bot_module = BotModule(
        bot_token, 
        chat_id, 
        storage_module,
        prompt_module, 
        log_module)
    bot_module.start()
