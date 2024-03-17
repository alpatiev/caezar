import os
import sys
import json
import time
import logging
import asyncio
import subprocess
from app import parse_config, update_pid
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from logger import LoggerModule
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
        self.job_queue = None
        self.scheduled_message = ""
        self.module_logger = None
        self.module_storage = None
        self.module_prompts = None
        self.module_publisher = None
        self.TG_TOKEN = None
        self.ID_ROOT_CHAT = None
        self.CHAT_CONTEXT_KEY_AUTH = None

    def start(self):
        self.__configure()
        self.__init_modules()
        self.__start_modules()
        self.__start_application()

    def stop(self):
        update_pid("")
        sys.exit(0)

    # ----------------------------------------------
    # SECTION: SETUPS

    def __configure(self):
        self.TG_TOKEN = self.config.get("authentification", {}).get("bot_token", None)
        self.ID_ROOT_CHAT = self.config.get("authentification", {}).get("root_chat", None)
        self.CHAT_CONTEXT_KEY_AUTH = self.config.get("message_context_key", {}).get("awaiting_auth", None)

    def __init_modules(self):
        self.module_storage = StorageModule()
        self.module_logger = LoggerModule()
        self.module_prompts = PromptModule()
        self.module_publisher = PublisherModule() 

    def __start_modules(self):
        self.module_storage.start(self.config)
        self.module_logger.start(self.config)
        self.module_prompts.start(self.config)
        self.module_publisher.start(self.config, self.__callback_root_chat)
        self.config = None

    def __start_application(self):
        self.application = Application.builder().token(self.TG_TOKEN).build()
        self.job_queue = self.application.job_queue
        self.__schedule_boot_message()
        self.application.add_handler(CommandHandler("start", self.__handler_command_start))
        self.application.add_handler(CommandHandler("help", self.__handler_command_help))
        self.application.add_handler(CommandHandler("select", self.__handler_command_select))
        self.application.add_handler(CommandHandler("system", self.__handler_command_system))
        self.application.add_handler(CommandHandler("update", self.__handler_command_update))
        self.application.add_handler(CommandHandler("reboot", self.__handler_command_reboot))
        self.application.add_handler(CommandHandler("shutdown", self.__handler_command_shutdown))
        self.application.add_handler(CallbackQueryHandler(self.__handler_callback_select_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__handler_typed_text))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.__handler_typed_image))
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    # ----------------------------------------------
    # SECTION: AUTH

    def __verified_chat(self, chat_id):
        lhs = f"{chat_id}"
        rhs = f"{self.ID_ROOT_CHAT}"
        return lhs == rhs

    # ----------------------------------------------
    # SECTION: COMMAND START

    async def __handler_command_start(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.module_prompts.msg_start_registered_bot_for_chat(chat_id)
            self.context = context
        else:
            reply = self.module_prompts.err_any_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    # ----------------------------------------------
    # SECTION: COMMAND HELP

    async def __handler_command_help(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.module_prompts.msg_cmd_help()
        else:
            reply = self.module_prompts.err_any_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    # ----------------------------------------------
    # COMMAND: SELECT

    async def __handler_command_select(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):        
            keyboard = [
                [
                    InlineKeyboardButton("1", callback_data="1"),
                ],
                [
                    InlineKeyboardButton("2", callback_data="2"),
                ],
                [
                    InlineKeyboardButton("3", callback_data="3"),
                ],
                [
                    InlineKeyboardButton("4", callback_data="4"),
                ],
                [
                    InlineKeyboardButton("5", callback_data="5"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            reply_prompt = self.module_prompts.msg_cmd_select_placeholder()
            await update.message.reply_text(reply_prompt, reply_markup=reply_markup)
        else:
            reply = self.module_prompts.err_any_unauthorized_chat() 
            await context.bot.send_message(chat_id=chat_id, text=reply)
    

    # ----------------------------------------------
    # COMMAND: SYSTEM

    async def __handler_command_system(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.module_prompts.msg_cmd_system()
        else:
            reply = self.module_prompts.err_any_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)
    
    # ----------------------------------------------
    # COMMAND: UPDATE
    
    async def __handler_command_update(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.module_prompts.msg_cmd_update()
        else:
            reply = self.module_prompts.err_any_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    # ----------------------------------------------
    # COMMAND: REBOOT
    
    async def __handler_command_reboot(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.module_prompts.msg_cmd_reboot()
        else:
            reply = self.module_prompts.err_any_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)
        update_pid("")
        subprocess.run(["reboot"])

    # ----------------------------------------------
    # COMMAND: SHUTDOWN

    async def __handler_command_shutdown(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.module_prompts.msg_cmd_shutdown()
        else:
            reply = self.module_prompts.err_any_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)
        update_pid("")
        subprocess.run(["reboot"])

    # ----------------------------------------------
    # HANDLERS: CALLBACKS

    async def __handler_callback_select_command(self, update: Update, context) -> None:
        query = update.callback_query
        option = query.data
        reply = self.module_prompts.msg_cmd_select_result(option)
        await query.answer()
        await query.edit_message_text(text=reply)

    # ----------------------------------------------
    # HANDLERS: MESSAGES

    async def __handler_typed_text(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.module_prompts.msg_any_echo_text(update.message.text)
        else:
            reply = self.module_prompts.err_any_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)        

    async def __handler_typed_image(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.module_prompts.msg_any_echo_image()
        else:
            reply = self.module_prompts.err_any_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)           
    
    # ----------------------------------------------
    # SECTION: PUBLISH METHODS

    def __schedule_boot_message(self):
        boot_message = self.module_prompts.msg_any_boot()
        with open('buffer.json', 'r+') as file:
            data = json.load(file)
            data['message_queue'].append(boot_message)
            file.seek(0)
            json.dump(data, file)

    def __callback_root_chat(self, message):
        try:
            self.scheduled_message = message
            self.application.job_queue.run_once(self.__root_chat_publisher, 0)
        except Exception as e:
            print("Error sending message:", e)       

    async def __root_chat_publisher(self, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=self.ID_ROOT_CHAT, text=self.scheduled_message)

# --------------------------------------------------
# SECTION: MAIN

if __name__ == "__main__":
    config = parse_config()
    bot = CaesarBot(config)
    bot.start()
