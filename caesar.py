import os
import sys
import json
import time
import logging
import asyncio
import subprocess
from app import parse_config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from logger import LogModule
from storer import StorageModule
from prompter import PromptModule
from publisher import PublisherModule

# --------------------------------------------------
# ENTITY: BOT
# Bot class that provides dispatching logic.
# Only one instance per one folder are allowed.

class CaesarBot:

    # ----------------------------------------------
    # SECTION: LIFECYCLE

    def __init__(self, config):
        self.config = config
        self.application = None
        self.module_logger = None
        self.module_storage = None
        self.module_prompts = None
        self.module_publisher = None
        self.bot_token = None
        self.root_chat = None

    def start(self):
        self.__start_init_modules()
        self.__start_observing()
        self.__start_logging()
        self.__run_application()

    def stop(self):
        sys.exit(0)

    # ----------------------------------------------
    # SECTION: SETUPS

    def __start_init_modules(self):
        print(self.config)
        self.debug_print_daemon()
        exit(0)
        self.config = None
        ##self.storage_module.connect_database()

    def debug_print_daemon(self):
        s = 0
        for _ in range(30):  # Corrected the syntax for the loop
            with open("debug.txt", 'w') as file:
                file.write(f"running for {s} seconds..")
            s += 1
            time.sleep(1)

    def __start_message_observing(self):  
        self.module_publisher = MessagePublisher(self.config_path, self.__received_new_shared_message) 
        self.module_publisher.start()

    def __start_logging(self):
        logging.basicConfig(format="[%(asctime)s] [%(levelname)s] [%(name)s] [%(message)s]", level=logging.INFO)
        logger = logging.getLogger(__name__)

    def __start_application(self):
        self.application = Application.builder().token(self.bot_token).build()
        self.__schedule_boot_message()
        self.application.add_handler(CommandHandler("start", self.__handler_command_start))
        self.application.add_handler(CommandHandler("help", self.__handler_command_help))
        self.application.add_handler(CommandHandler("select", self.__handler_command_select))
        self.application.add_handler(CommandHandler("debug", self.__handler_command_debug))
        self.application.add_handler(CommandHandler("reboot", self.__handler_command_reboot))
        self.application.add_handler(CallbackQueryHandler(self.__handler_callback_select_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__handler_typed_text))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.__handler_typed_image))
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    # ----------------------------------------------
    # SECTION: AUTH

    def __verified_chat(self, chat_id):
        lhs = f"{chat_id}"
        rhs = f"{self.chat_id}"
        return lhs == rhs
    
    # ----------------------------------------------
    # SECTION: COMMAND HANDLERS

    async def __handler_command_start(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_start_registered_bot_for_chat(chat_id)
            self.context = context
        else:
            reply = self.prompt_module.err_common_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    async def __handler_command_help(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_help_show_help_info()
        else:
            reply = self.prompt_module.err_common_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    async def __handler_command_select(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):        
            keyboard = [
                [
                    InlineKeyboardButton("1", callback_data="1"),
                    InlineKeyboardButton("2", callback_data="2"),
                    InlineKeyboardButton("3", callback_data="3"),
                    InlineKeyboardButton("4", callback_data="4"),
                    InlineKeyboardButton("5", callback_data="5"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            reply_prompt = self.prompt_module.msg_select_choose_placeholder()
            await update.message.reply_text(reply_prompt, reply_markup=reply_markup)
        else:
            reply = self.prompt_module.err_common_unauthorized_chat() 
            await context.bot.send_message(chat_id=chat_id, text=reply)
    
    async def __handler_command_debug(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_debug_show_system_info()
        else:
            reply = self.prompt_module.err_common_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    async def __handler_command_reboot(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_reboot_server()
            
        else:
            reply = self.prompt_module.err_common_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)
        subprocess.run(["reboot"])

    # ----------------------------------------------
    # SECTION: CALLBACK HANDLERS

    async def __handler_callback_select_command(self, update: Update, context) -> None:
        query = update.callback_query
        option = query.data
        reply = self.prompt_module.msg_select_chosen(option)
        await query.answer()
        await query.edit_message_text(text=reply)

    # ----------------------------------------------
    # SECTION: MESSAGE HANDLERS

    async def __handler_typed_text(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_common_echo_message(update.message.text)
        else:
            reply = self.prompt_module.err_common_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)        

    async def __handler_typed_image(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_common_echo_image()
        else:
            reply = self.prompt_module.err_common_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)           
    
    # ----------------------------------------------
    # SECTION: PUBLISH METHODS

    def __schedule_boot_message(self):
        boot_message = self.module_prompts.msg_start_system_is_up()
        with open('buffer.json', 'r+') as file:
            data = json.load(file)
            data['message_queue'].append(boot_message)
            file.seek(0)
            json.dump(data, file)

    def __received_new_shared_message(self, message):
        try:
            formatted_message = self.module_prompts.msg_common_received_text_from_queue(message)
            asyncio.run(self.__send_message(self.chat_id, formatted_message))
        except Exception as e:
            print("Error sending message:", e)       

    async def __send_message(self, chat_id, message):
        await self.application.bot.send_message(chat_id=chat_id, text=message)
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# --------------------------------------------------
# SECTION: MAIN
# Just run the script.

if __name__ == "__main__":
    config = parse_config()
    bot = CaesarBot(config)
    bot.start()
