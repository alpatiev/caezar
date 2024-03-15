# INFO: Prompt module 
# Creates replies and user messages

class PromptModule:
    # SECTION: MESSAGES - /start
    # [msg_start_<name>()]
    
    @staticmethod
    def msg_start_enter_password_placeholder():
        return "Enter your client password:"

    @staticmethod
    def msg_start_registered_bot_for_chat(chat_id):
        return f"Sucessfully configured bot for chat {chat_id}."

    # SECTION: MESSAGES - /help
    # [msg_help_<name>()]

    @staticmethod
    def msg_help_show_help_info():
        return """
/start    - Start private bot
/help     - Get a list of available commands
/server   - Change selected API
/info     - Show all API info
/api_key  - Updates API key
/debug    - Shows current request info
/run      - Runs current job
"""

    # SECTION: MESSAGES - /server
    # [msg_server_<name>()]

    # SECTION: MESSAGES - /info
    # [msg_info_<name>()]

    # SECTION: MESSAGES - /api_key
    # [msg_api_key_<name>()]

    # SECTION: MESSAGES - /debug
    # [msg_debug_<name>()]

    # SECTION: MESSAGES - /run
    # [msg_run_<name>()]

    @staticmethod
    def msg_run_begin_task(target, prompt, image):
        return "Start processing task..."

    # SECTION: ERRORS - /start
    # [err_start_<name>()]

    @staticmethod
    def err_start_unknown_exception(error):
        return f"""
Error. Cannot start this bot.
*****************************
{error}
*****************************
Reach out @alpatievvv to report the issue.
"""
    @staticmethod
    def err_start_invalid_password():
        return """
Invalid password. 
Reach out @alpatievvv to get this.
"""

    # SECTION: ERRORS - /help
    # [err_help_<name>()]

    # SECTION: ERRORS - /server
    # [err_server_<name>()]

    # SECTION: ERRORS - /info
    # [err_info_<name>()]

    # SECTION: ERRORS - /api_key
    # [err_api_key_<name>()]

    @staticmethod
    def err_api_key_invalid():
        return "Invalid api key provided."

    # SECTION: ERRORS - /debug
    # [err_debug_<name>()]

    # SECTION: ERRORS - /run
    # [err_run_<name>()]
