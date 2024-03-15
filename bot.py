import sys
import json
import time
import logging
import asyncio
import constants
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
        self.bot = None
        self.image_buffer = None
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
        target_path = constants.PATH_MESSAGE_QUEUE
        self.queue_module = QueueObserver(target_path, self.__recieved_new_shared_message) 
        self.queue_module.start()

    def __start_logging(self):
        logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
        logger = logging.getLogger(__name__)

    def __run_application(self):
        application = Application.builder().token(self.bot_token).build()
        application.add_handler(CommandHandler("start", self.__handler_command_start))
        application.add_handler(CommandHandler("help", self.__handler_command_help))
        application.add_handler(CommandHandler("info", self.__handler_command_info))
        application.add_handler(CommandHandler("debug", self.__handler_command_debug))
        application.add_handler(CommandHandler("server", self.__handler_command_server))
        application.add_handler(CommandHandler("api_key", self.__handler_command_api_key))
        application.add_handler(CommandHandler("image", self.__handler_command_image))
        application.add_handler(CommandHandler("prompt", self.__handler_command_prompt))
        application.add_handler(CommandHandler("run", self.__handler_command_run))
        application.add_handler(CallbackQueryHandler(self.__handler_callback_mode))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.__handler_typed_text))
        application.add_handler(MessageHandler(filters.PHOTO, self.__handler_typed_image))
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        self.bot = application.bot

    # ----------------------------------------------
    # SECTION: Configure methods

    def __verified_auth(self, auth_key):
        print(self.auth_key, auth_key)
        return auth_key == self.auth_key

    def __verify_chat(self, chat_id):
        result = self.storage_module.update_selected_id(chat_id)

    def __verified_chat(self, chat_id):
        #ids = self.storage_module.fetch_all_ids()
        #id_str = f"{chat_id}"
        #return id_str in ids
        return self.chat_id is chat_id
    
    # ----------------------------------------------
    # SECTION: Command handlers

    async def __handler_command_start(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        print(chat_id)
        placeholder = self.prompt_module.msg_start_enter_password_placeholder()
        await context.bot.send_message(chat_id=chat_id, text=placeholder)
        context.user_data[constants.BOT_CONTEXT_KEY_AUTHORIZING] = True

    async def __handler_command_help(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_help_show_help_info()
        else:
            reply = self.prompt_module.err_reply_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    async def __handler_command_info(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_info_stub_message()
        else:
            reply = self.prompt_module.err_reply_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    async def __handler_command_debug(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_debug_stub_message()
        else:
            reply = self.prompt_module.err_reply_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    async def __handler_command_server(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):        
            keyboard = [
                [InlineKeyboardButton(
                    constants.API_ID_STABILITY_AI,
                    callback_data=constants.API_ID_STABILITY_AI
                    ),
                InlineKeyboardButton(
                    constants.API_ID_LOCAL_PROCESSING,
                    callback_data=constants.API_ID_LOCAL_PROCESSING
                    )   
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            reply_prompt = self.prompt_module.msg_server_choose_placeholder()
            await update.message.reply_text(reply_prompt, reply_markup=reply_markup)
        else:
            reply = self.prompt_module.err_reply_unauthorized_chat() 
            await context.bot.send_message(chat_id=chat_id, text=reply)
    
    async def __handler_command_api_key(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
                placeholder = self.prompt_module.msg_api_key_enter_placeholder()
                await context.bot.send_message(chat_id=chat_id, text=placeholder)
                context.user_data[constants.BOT_CONTEXT_KEY_AWAITING_API_KEY] = True 
        else:
            error = self.prompt_module.err_reply_unauthorized_chat() 
            await context.bot.send_message(chat_id=chat_id, text=error)

    async def __handler_command_prompt(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
                placeholder = self.prompt_module.msg_prompt_enter_placeholder()
                await context.bot.send_message(chat_id=chat_id, text=placeholder)
                context.user_data[constants.BOT_CONTEXT_KEY_AWAITING_PROMPT] = True 
        else:
            error = self.prompt_module.err_reply_unauthorized_chat() 
            await context.bot.send_message(chat_id=chat_id, text=error)

    async def __handler_command_image(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
                placeholder = self.prompt_module.msg_image_enter_placeholder()
                await context.bot.send_message(chat_id=chat_id, text=placeholder)
                context.user_data[constants.BOT_CONTEXT_KEY_AWAITING_IMAGE] = True 
        else:
            error = self.prompt_module.err_reply_unauthorized_chat() 
            await context.bot.send_message(chat_id=chat_id, text=error)

    async def __handler_command_run(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        if self.__verified_chat(chat_id):
            reply = self.prompt_module.msg_run_begin_task()
        else:
            reply = self.prompt_module.err_reply_unauthorized_chat() 
        await context.bot.send_message(chat_id=chat_id, text=reply)

    # ----------------------------------------------
    # SECTION: Callback handlers

    async def __handler_callback_mode(self, update: Update, context) -> None:
        query = update.callback_query
        mode = query.data
        reply = self.prompt_module.msg_server_chosen(mode)
        await query.answer()
        await query.edit_message_text(text=reply)

    # ----------------------------------------------
    # SECTION: Message handlers

    async def __handler_typed_text(self, update: Update, context) -> None:
        auth_state = constants.BOT_CONTEXT_KEY_AUTHORIZING
        api_key_state = constants.BOT_CONTEXT_KEY_AWAITING_API_KEY
        prompt_state = constants.BOT_CONTEXT_KEY_AWAITING_PROMPT
        chat_id = update.message.chat_id

        if context.user_data[auth_state] is not None:
            if self.__verified_auth(update.message.text):
                if auth_state in context.user_data and context.user_data[auth_state]:
                    context.user_data[auth_state] = None
                    success = self.prompt_module.msg_start_registered_bot_for_chat(chat_id)
                    self.__verify_chat(chat_id)
                    await context.bot.send_message(chat_id=chat_id, text=success)    
            else:
                unauthorized_reply = self.prompt_module.err_start_invalid_password()
                await context.bot.send_message(chat_id=chat_id, text=unauthorized_reply)
                return

        if self.__verified_chat(chat_id):
            if api_key_state in context.user_data and context.user_data[api_key_state]:
                context.user_data[api_key_state] = None
                success = self.prompt_module.msg_api_key_update_success()
                await context.bot.send_message(chat_id=chat_id, text=success)
            elif prompt_state in context.user_data and context.user_data[prompt_state]:
                context.user_data[prompt_state] = None
                success = self.prompt_module.msg_prompt_update_success()
                await context.bot.send_message(chat_id=chat_id, text=success)
            else:
                return
        else:
            unauthorized_reply = self.prompt_module.err_reply_unauthorized_chat()
            await context.bot.send_message(chat_id=chat_id, text=unauthorized_reply)

    async def __handler_typed_image(self, update: Update, context) -> None:
        chat_id = update.message.chat_id
        image_state = constants.BOT_CONTEXT_KEY_AWAITING_IMAGE
        if self.__verified_chat(chat_id):
            if image_state in context.user_data and context.user_data[image_state]:
                photo_objects = update.message.photo
                photo_file = await context.bot.get_file(photo_objects[-1])
                if photo_file.file_path.endswith('.jpg') or photo_file.file_path.endswith('.jpeg'): 
                    file_size_bytes = photo_file.file_size
                    file_size_kb = file_size_bytes / 1024 
                    await context.bot.send_chat_action(chat_id=update.message.chat_id, action="typing")
                    time.sleep(5)
                    # result_image = open("temp.jpg", "rb")
                    result_image = photo_file
                    context.user_data[image_state] = None
                    success = self.prompt_module.msg_image_upload_success(file_size_kb)
                    await context.bot.send_message(chat_id=chat_id, text=success) 
                    #await context.bot.send_photo(chat_id=update.message.chat_id, photo=result_image, caption=f"Result {file_size_kb:.2f} kb")
                else:
                    await context.bot.send_message(chat_id=update.message.chat_id, text="Incorrect format, expected JPG")   
        else:
            unauthorized_reply = self.prompt_module.err_start_invalid_password()
            await context.bot.send_message(chat_id=chat_id, text=unauthorized_reply)           
    
    # ----------------------------------------------
    # SECTION: Message queue handlers

    def __recieved_new_shared_message(self, message):
        print(f">> {message}")
