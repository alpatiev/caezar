import os
import psutil
from datetime import datetime
from module import BotModule

# --------------------------------------------------
# ENTITY: PROMPT
# Creates replies and user messages

class PromptModule(BotModule):
    
    # ----------------------------------------------
    # SECTION: LIFECYCLE

    def __init__(self):
        pass

    def start(self, config):
        print(">>> module_prompt started..")

    def stop(self):
        print(">>> module_prompt stopped")

    # ----------------------------------------------
    # SECTION: MESSAGES - /start

    @staticmethod
    def msg_start_success(chat_id):
        return f"✅ Started bot for chat {chat_id}"

    @staticmethod
    def msg_start_report():
        system_info = os.uname()
        machine = system_info.nodename
        system_time = datetime.now().strftime("%B %d %Y %H:%M")
        mem = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        total_mem = "{:.2f}".format(mem.total / (1024 * 1024))
        available_mem = "{:.2f}".format(mem.available / (1024 * 1024))
        used_mem = "{:.2f}".format(mem.used / (1024 * 1024))
        return f"""
✅ SYSTEM IS UP
🕑 {system_time}
⚙️ {machine}

CPU stats:
➖ load {cpu_percent}$

RAM stats, MB: 
➖ total {total_mem}
➖ available {available_mem}
➖ used {used_mem} 
"""

    # ----------------------------------------------
    # SECTION: MESSAGES - /help

    @staticmethod
    def msg_cmd_help():
        return """
/start ➖ start private bot
/help ➖ show list of commands
/select ➖ choose task to execute
/system ➖ show system info
/reboot ➖ reboot system (OS)
/update ➖ update and reboot bot
/shutdown ➖ shut down the bot
"""

    # ----------------------------------------------
    # SECTION: MESSAGES - /select

    @staticmethod
    def msg_cmd_select_placeholder():
        return "❔ Select task:"

    @staticmethod
    def msg_cmd_select_result(option_name):
        return f"✅ Starting {option_name}.."

    # ----------------------------------------------
    # SECTION: MESSAGES - /system

    @staticmethod
    def msg_cmd_system():
        system_info = os.uname()
        machine = system_info.nodename
        system_time = datetime.now().strftime("%B %d %Y %H:%M")
        mem = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent()
        total_mem = "{:.2f}".format(mem.total / (1024 * 1024))
        available_mem = "{:.2f}".format(mem.available / (1024 * 1024))
        used_mem = "{:.2f}".format(mem.used / (1024 * 1024))
        return f"""
ℹ️ SYSTEM INFO
🕑 {system_time}
⚙️ {machine}

CPU stats:
➖ load {cpu_percent}$

RAM stats, MB: 
➖ total {total_mem}
➖ available {available_mem}
➖ used {used_mem} 
"""
    
    # ----------------------------------------------
    # SECTION: MESSAGES - /reboot

    @staticmethod
    def msg_cmd_reboot():
        return "⏳ Restarting the server.."

    # ----------------------------------------------
    # SECTION: MESSAGES - /shutdown

    @staticmethod
    def msg_cmd_shutdown():
        return "⏳ Restarting the server.."

    # ----------------------------------------------
    # SECTION: MESSAGES - common messages

    @staticmethod
    def msg_any_echo_text(message):
        return f"❔ {message}"

    @staticmethod
    def msg_any_echo_image():
        #file_size_kb = image.sizr
        #return f"❔ {file_size_kb} kb"
        return f"❔ Image"

    # ----------------------------------------------
    # SECTION: ERRORS

    @staticmethod
    def err_start_unknown_exception(error):
        return f"""
❌ Cannot start this bot. {error}
Reach out @alpatievvv to support.
"""

    @staticmethod
    def err_any_unauthorized_chat():
        return """
❌ Unauthorized user.
Reach out @alpatievvv for support.
"""