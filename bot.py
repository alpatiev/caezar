import sys
import json
import time
import logging
import asyncio
import const
import subprocess
from observer import QueueObserver
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# --------------------------------------------------
# NOTE: Storage module
# Bot class that provides dispatching logic
#
class BotModule:
    def __init__(self, bot_token, chat_id, storage_module, prompt_module, log_module):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.image_buffer = None
        self.context = None
        self.application = None
        self.storage_module = storage_module
        self.prompt_module = prompt_module
        self.log_module = log_module

    # ----------------------------------------------
    # SECTION: Start application

    def start(self):
        self.storage_module.connect_database()
        self.__start_observing()
        self.__start_logging()
        self.__run_application()

    # ----------------------------------------------
    # SECTION: Configure methods

    def __start_observing(self):  
        target_path = const.PATH_MESSAGE_QUEUE
        self.queue_module = QueueObserver(target_path, self.__received_new_shared_message) 
        self.queue_module.start()

    def __start_logging(self):
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
        logger = logging.getLogger(__name__)

    def __run_application(self):
        self.application = Application.builder().token(self.bot_token).build()
        self.application.add_handler(CommandHandler("start", self.__handler_command_start))
        self.application.add_handler(CommandHandler("help", self.__handler_command_help))
        self.application.add_handler(CommandHandler("select", self.__handler_command_select))
        self.application.add_handler(CommandHandler("debug", self.__handler_command_debug))
        self.application.add_handler(CommandHandler("reboot", self.__handler_command_reboot))
        self.application.add_handler(CallbackQueryHandler(self.__handler_callback_select_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__handler_typed_text))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.__handler_typed_image))
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
        boot_message = self.prompt_module.msg_start_system_is_up()
        self.send_message(chat_id, boot_message)

    # ----------------------------------------------
    # SECTION: Authorization methods

    def __verified_chat(self, chat_id):
        lhs = f"{chat_id}"
        rhs = f"{self.chat_id}"
        return lhs == rhs
    
    # ----------------------------------------------
    # SECTION: Command handlers

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
    # SECTION: Callback handlers

    async def __handler_callback_select_command(self, update: Update, context) -> None:
        query = update.callback_query
        option = query.data
        reply = self.prompt_module.msg_select_chosen(option)
        await query.answer()
        await query.edit_message_text(text=reply)

    # ----------------------------------------------
    # SECTION: Message handlers

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
    # SECTION: Message queue handlers

    def __received_new_shared_message(self, message):
        try:
            formatted_message = self.prompt_module.msg_common_received_text_from_queue(message)
            asyncio.run(self.send_message(self.chat_id, formatted_message))
        except Exception as e:
            print("Error sending message:", e)       

    async def send_message(self, chat_id, message):
        await self.application.bot.send_message(chat_id=chat_id, text=message)
        self.application.run_polling()
