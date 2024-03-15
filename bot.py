import sys
import json
import time
import logging
import CONSTANTS
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# INFO: Storage module
# Bot class that provides dispatching logic

class BotModule:
    def __init__(self, bot_token, auth_admin_key, storage_module, prompt_module, log_module):
        self.bot_token = bot_token
        self.auth_admin_key = auth_admin_key
        self.image_buffer = None
        self.storage_module = storage_module
        self.prompt_module = prompt_module
        self.log_module = log_module

    # Start the bot

    def start(self):
        self.storage_module.connect_database()
        self.__start_logging()
        self.__run_application()

    # Configure methods
    
    def __start_logging(self):
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
        logger = logging.getLogger(__name__)
   
    def __run_application(self):
        application = Application.builder().token(self.bot_token).build()
        application.add_handler(CommandHandler("start", handler_command_start))
        application.add_handler(CommandHandler("help", handler_command_help))
        application.add_handler(CommandHandler("service", handler_command_mode))
        application.add_handler(CallbackQueryHandler(handler_callback_mode))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler_typed_text))
        application.add_handler(MessageHandler(filters.PHOTO, handler_typed_image))
        application.run_polling(allowed_updates=Update.ALL_TYPES)

    # MARK: - Command handlers

    async def handler_command_start(update: Update, context) -> None:
        chat_id = update.message.chat_id
        await context.bot.send_message(chat_id=update.message.chat_id, text=CONSTANTS.MSG_STUB_LOGIN)

    async def handler_command_help(update: Update, context) -> None:
        await context.bot.send_message(chat_id=update.message.chat_id, text=CONSTANTS.MSG_STUB_HELP_LIST)

    async def handler_command_mode(update: Update, context) -> None:
        keyboard = []
        for mode_data in config.bot_polling_mode:
            button = InlineKeyboardButton(mode_data['title'], callback_data=mode_data['action'])
            keyboard.append([button])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Choose bot mode: ", reply_markup=reply_markup)

    # MARK: - Callback handlers

    async def handler_callback_mode(update: Update, context) -> None:
        query = update.callback_query
        mode = query.data
        await query.answer()
        await query.edit_message_text(text=f"Selected mode: {mode}")

    # MARK: - Message handlers

    async def handler_typed_text(update: Update, context) -> None:
        await context.bot.send_message(chat_id=update.message.chat_id, text=CONSTANTS.MSG_STUB_HELP_LIST)
        await update.message.reply_text("Not a command. Type /help")

    async def handler_typed_image(update: Update, context) -> None:
        photo_objects = update.message.photo
        photo_file = await context.bot.get_file(photo_objects[-1])
        if photo_file.file_path.endswith('.jpg') or photo_file.file_path.endswith('.jpeg'): 
            file_size_bytes = photo_file.file_size
            file_size_kb = file_size_bytes / 1024 
            await update.message.reply_text(f"Processing image {file_size_kb:.2f} kb from {update.message.chat_id}..")
            await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
            time.sleep(3)
            # result_image = open("temp.jpg", "rb")
            result_image = photo_file
            await context.bot.send_message(chat_id=update.message.chat_id, text="Incorrect format, expected JPG")   
            #await context.bot.send_photo(chat_id=update.message.chat_id, photo=result_image, caption=f"Result {file_size_kb:.2f} kb")
        else:
            await context.bot.send_message(chat_id=update.message.chat_id, text="Incorrect format, expected JPG")   
