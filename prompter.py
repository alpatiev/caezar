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
        return 0

    def stop(self):
        return 0

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
        ram_percent = mem.percent
        return f"""
✅ SYSTEM IS UP
🕑 {system_time}
⚙️ {machine}

CPU stats:
➖ load  {cpu_percent}%

RAM stats: 
➖ load  {ram_percent}%
➖ total  {total_mem} MB
➖ free   {available_mem} MB
➖ used  {used_mem} MB
"""

    # ----------------------------------------------
    # SECTION: MESSAGES - /help

    @staticmethod
    def msg_cmd_help():
        return """
/start ➖ start this bot
/help ➖ show list of commands
/select ➖ choose task to execute
/system ➖ show system info
/reboot ➖ reboot host machine
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
        ram_percent = mem.percent
        return f"""
ℹ️ SYSTEM INFO
🕑 {system_time}
⚙️ {machine}

CPU stats:
➖ load  {cpu_percent}%

RAM stats: 
➖ load  {ram_percent}%
➖ total  {total_mem} MB
➖ free   {available_mem} MB
➖ used  {used_mem} MB
"""
    
    # ----------------------------------------------
    # SECTION: MESSAGES - /reboot

    @staticmethod
    def msg_cmd_reboot_placeholder():
        return "⚠️ Confirm server reboot:"

    @staticmethod
    def msg_cmd_reboot_confirmed():
        return "🔄 Restarting the the server.."

    @staticmethod
    def msg_cmd_reboot_cancelled():
        return "❕ Server reboot cancelled."
    # ----------------------------------------------
    # SECTION: MESSAGES - /shutdown

    @staticmethod
    def msg_cmd_shutdown_placeholder():
        return "⚠️ Confirm bot shutdown:"

    @staticmethod
    def msg_cmd_shutdown_confirmed():
        return "💀 Shutting down the bot.."

    @staticmethod
    def msg_cmd_shutdown_cancelled():
        return "❕ Bot shutdown cancelled."

    # ----------------------------------------------
    # SECTION: MESSAGES - common messages

    @staticmethod
    def msg_any_echo_text(message):
        return f"❔ {message}"

    @staticmethod
    def msg_any_echo_image():
        return f"❔ Image"

    # ----------------------------------------------
    # SECTION: ERRORS

    @staticmethod
    def err_start_unknown_exception(error):
        return f"❌ Cannot start this bot. Reach out @alpatievvv for support. {error}."

    @staticmethod
    def err_any_unauthorized_chat():
        return "❌ Unauthorized user. Reach out @alpatievvv for support."
