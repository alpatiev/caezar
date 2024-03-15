import psutil
from datetime import datetime

# --------------------------------------------------
# INFO: Prompt module 
# Creates replies and user messages

class PromptModule:
    def __init__(self):
        pass

    # ----------------------------------------------
    # SECTION: MESSAGES - /start
    # [msg_start_<name>()]

    @staticmethod
    def msg_start_registered_bot_for_chat(chat_id):
        return f"✅ Started bot for chat {chat_id}"

    @staticmethod
    def msg_start_system_is_up():
        system_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        mem = psutil.virtual_memory()
        total_mem = "{:.2f}".format(mem.total / (1024 * 1024))
        available_mem = "{:.2f}".format(mem.available / (1024 * 1024))
        used_mem = "{:.2f}".format(mem.used / (1024 * 1024))
        return f"""
-------------------------------------
✅ {system_time} SYSTEM IS UP
-------------------------------------
RAM stats   :
Total       : {total_mem} MB
Available   : {available_mem} MB
Used        : {used_mem} MB
-------------------------------------
"""

    # ----------------------------------------------
    # SECTION: MESSAGES - /help
    # [msg_help_<name>()]

    @staticmethod
    def msg_help_show_help_info():
        return """
/start - start private bot
/help - show list of commands
/select - choose option
/debug - show debug logs
/reboot - reboot server
"""

    # ----------------------------------------------
    # SECTION: MESSAGES - /select
    # [msg_select_<name>()]
    @staticmethod
    def msg_select_choose_placeholder():
        return "❔ Choose option:"

    @staticmethod
    def msg_select_chosen(option_id):
        return f"✅ Selected {option_id}."

    # ----------------------------------------------
    # SECTION: MESSAGES - /debug
    # [msg_debug_<name>()]
    @staticmethod
    def msg_debug_show_system_info():
        netw_list = ','.join(f"[{addr.address}]" for addresses in psutil.net_if_addrs().values() for addr in addresses)
        formatted_addresses = '\n'.join(netw_list.split(',')[:10])
        cpu_percent = psutil.cpu_percent()
        cpu_count = psutil.cpu_count()
        mem = psutil.virtual_memory()
        total_mem = "{:.2f}".format(mem.total / (1024 * 1024))
        available_mem = "{:.2f}".format(mem.available / (1024 * 1024))
        used_mem = "{:.2f}".format(mem.used / (1024 * 1024))
        return f"""
-------------------------------------
Running on Ubuntu 22.04
-------------------------------------
CPU usage   : {cpu_percent}%
CPU count   : {cpu_count}
-------------------------------------
RAM stats   :
Total       : {total_mem} MB
Available   : {available_mem} MB
Used        : {used_mem} MB
-------------------------------------
{formatted_addresses}
-------------------------------------
"""

    # ----------------------------------------------
    # SECTION: MESSAGES - /reboot
    # [msg_select_<name>()]
    @staticmethod
    def msg_reboot_server():
        return "⏳ Restarting the server.."

    # ----------------------------------------------
    # SECTION: MESSAGES - common messages
    # [msg_common_<name>()]

    @staticmethod
    def msg_common_echo_message(message):
        return f"❔ {message}"

    @staticmethod
    def msg_common_echo_image():
        #file_size_kb = image.sizr
        #return f"❔ {file_size_kb} kb"
        return f"❔ Image"

    @staticmethod
    def msg_common_received_text_from_queue(message):
        return message

    # ----------------------------------------------
    # SECTION: ERRORS - /start
    # [err_start_<name>()]

    @staticmethod
    def err_start_unknown_exception(error):
        return f"""
❌ Error: Cannot start this bot
-------------------------------------
{error}
-------------------------------------
Reach out @alpatievvv to report
"""

    # ----------------------------------------------
    # SECTION: ERRORS - /help
    # [err_help_<name>()]
    
    # ----------------------------------------------
    # SECTION: ERRORS - /select
    # [err_select_<name>()]

    # ----------------------------------------------
    # SECTION: ERRORS - /debug
    # [err_debug_<name>()]

    # ----------------------------------------------
    # SECTION: ERRORS - /reboot
    # [err_reboot_<name>()]

    # ----------------------------------------------
    # SECTION: ERRORS - common
    # [err_common_<name>()]

    @staticmethod
    def err_common_unauthorized_chat():
        return """
❌ Unauthorized user 
Reach out @alpatievvv to get password
"""