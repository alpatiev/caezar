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
    def msg_start_enter_password_placeholder():
        return "Enter auth password:"

    @staticmethod
    def msg_start_registered_bot_for_chat(chat_id):
        return f"✅ Sucessfully configured bot for chat {chat_id}."

    # ----------------------------------------------
    # SECTION: MESSAGES - /help
    # [msg_help_<name>()]

    @staticmethod
    def msg_help_show_help_info():
        return """
/start - start private bot
/help - get a list of available commands
/info - show all API info
/debug - show debug logs and dump request
/server - change selected API
/api_key - update API key
/prompt - enter prompt
/image - enter image
/run - run current job
"""

    # ----------------------------------------------
    # SECTION: MESSAGES - /server
    # [msg_server_<name>()]
    @staticmethod
    def msg_server_choose_placeholder():
        return "Choose service to run:"

    @staticmethod
    def msg_server_chosen(server_name):
        return f"✅ {server_name}"

    # ----------------------------------------------
    # SECTION: MESSAGES - /info
    # [msg_info_<name>()]

    @staticmethod
    def msg_info_stub_message():
        return """
+-----------------+-----------------------------------------+
|    component    |              specification              |
+-----------------+-----------------------------------------+
| ~ Processor     | Intel Core i9-12900K @ 3.20GHz (16C/24T)|
| ~ Motherboard   | ASUS ROG Maximus Z690 Extreme           |
| ~ Memory        | 64 GB DDR5 RAM @ 6400 MHz               |
| ~ Graphics Card | NVIDIA GeForce RTX 4090 with 24GB GDDR6X|
| ~ Storage       | 2 TB NVMe SSD (PCIe 4.0) + 8 TB HDD     |
| ~ Power Supply  | Corsair AX1600i 1600W Platinum          |
| ~ OS type       | Ubuntu 22.04 LTS                        |
| ~ Display       | ASUS ROG Swift PG32UQX 32" 4K 144Hz HDR |
| ~ Cooling       | NZXT Kraken Z73 Liquid Cooler (360mm)   |
| ~ Case          | Phanteks Enthoo Elite Full Tower        |
+-----------------+-----------------------------------------+
"""
    # ----------------------------------------------
    # SECTION: MESSAGES - /debug
    # [msg_debug_<name>()]

    @staticmethod
    def msg_debug_stub_message():
        return """
2024-03-15 07:46:59,139 - INFO - Application started
2024-03-15 07:47:09,534 - INFO - HTTP Request: POST
2024-03-15 07:47:13,833 - INFO - HTTP Request: POST
2024-03-15 07:47:14,134 - INFO - HTTP Request: POST
2024-03-15 07:47:19,876 - INFO - HTTP Request: POST
2024-03-15 07:47:20,197 - INFO - HTTP Request: POST
2024-03-15 07:47:26,359 - INFO - HTTP Request: POST
2024-03-15 07:47:26,667 - INFO - HTTP Request: POST
2024-03-15 07:47:36,564 - INFO - HTTP Request: POST
2024-03-15 07:47:38,817 - INFO - HTTP Request: POST
2024-03-15 07:47:39,091 - INFO - HTTP Request: POST
2024-03-15 07:47:47,018 - INFO - HTTP Request: POST
2024-03-15 07:47:51,569 - INFO - HTTP Request: POST
2024-03-15 07:47:57,563 - INFO - HTTP Request: POST
"""

    # ----------------------------------------------
    # SECTION: MESSAGES - /api_key
    # [msg_api_key_<name>()]

    @staticmethod
    def msg_api_key_enter_placeholder():
        return "Enter api key:"

    @staticmethod
    def msg_api_key_update_success():
        return "✅ New API key is set up."
    # ----------------------------------------------
    # SECTION: MESSAGES - /prompt
    # [msg_prompt_<name>()]

    @staticmethod
    def msg_prompt_enter_placeholder():
        return "Enter your prompt:"

    @staticmethod
    def msg_prompt_update_success():
        return "✅ Successfully updated prompt."
    # ----------------------------------------------
    # SECTION: MESSAGES - /image
    # [msg_image_<name>()]

    @staticmethod
    def msg_image_enter_placeholder():
        return "Send image in .JPG format:"
    
    @staticmethod
    def msg_image_upload_success(image_size_kb):
        return f"✅ Uploaded image {image_size_kb} kb."

    # ----------------------------------------------
    # SECTION: MESSAGES - /run
    # [msg_run_<name>()]

    @staticmethod
    def msg_run_begin_task(target, prompt, image):
        return "Start processing task..."
    
    @staticmethod
    def msg_run_finish_task():
        return "✅ Successfully processed given data."

    # ----------------------------------------------
    # SECTION: MESSAGES - reply
    # [msg_reply_<name>()]

    # ----------------------------------------------
    # SECTION: ERRORS - /start
    # [err_start_<name>()]

    @staticmethod
    def err_start_unknown_exception(error):
        return f"""
❌ Error. Cannot start this bot.
*****************************
{error}
*****************************
Reach out @alpatievvv to report the issue.
"""
    @staticmethod
    def err_start_invalid_password():
        return """
⛔️ Invalid password. 
"""

    # ----------------------------------------------
    # SECTION: ERRORS - /help
    # [err_help_<name>()]

    # ----------------------------------------------
    # SECTION: ERRORS - /info
    # [err_info_<name>()]

    # ----------------------------------------------
    # SECTION: ERRORS - /debug
    # [err_debug_<name>()]

    # ----------------------------------------------
    # SECTION: ERRORS - /server
    # [err_server_<name>()]

    # SECTION: ERRORS - /api_key
    # [err_api_key_<name>()]

    @staticmethod
    def err_api_key_invalid():
        return """
❌ Invalid api key provided.
Try again or ask @alpatievvv.
"""

    # ----------------------------------------------
    # SECTION: MESSAGES - /prompt
    # [err_prompt_<name>()]

    # ----------------------------------------------
    # SECTION: MESSAGES - /image
    # [err_image_<name>()]

    # ----------------------------------------------
    # SECTION: ERRORS - /run
    # [err_run_<name>()]

    # ----------------------------------------------
    # SECTION: ERRORS - reply
    # [err_reply_<name>()]

    @staticmethod
    def err_reply_unauthorized_chat():
        return """
❌ Unauthorized chat. 
Reach out @alpatievvv to get password.
"""