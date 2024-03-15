# --------------------------------------------------
# SECTION: Resources
# [PATH_<NAME>] 

PATH_DATABASE = "database.sqlite"
PATH_MESSAGE_QUEUE = "buffer.json"

# --------------------------------------------------
# SECTION: Database keys
# [DB_KEY_<NAME>]

DB_TABLE_KEY_ID_LIST = "ids"
DB_TABLE_KEY_USERS_LIST = "chats"
DB_TABLE_KEY_LOGS_LIST  = "logs"
DB_ROW_KEY_USER_IMAGE_PATH = "image_path"
DB_ROW_KEY_USER_PIPELINE = "pipeline"
DB_ROW_KEY_USER_PROMPT = "prompt"
DB_ROW_KEY_LOG_MESSAGE = "log_message"

# --------------------------------------------------
# SECTION: LOGS - Log event keys
# [LOG_EVENT_KEY_<NAME>]

LOG_EVENT_KEY_SUCCESS = "SUCCESS_"
LOG_EVENT_KEY_WARING = "WARINING"
LOG_EVENT_KEY_ERROR = "ERROR___"
LOG_EVENT_KEY_INFO = "INFO____"

# --------------------------------------------------
# SECTION: LOGS - Bot context keys
# [BOT_CONTEXT_KEY_<NAME>]

BOT_CONTEXT_KEY_AUTHORIZING = "awaiting_password"
BOT_CONTEXT_KEY_AWAITING_API_KEY = "awaiting_key"
BOT_CONTEXT_KEY_AWAITING_PROMPT = "awaiting_prompt"
BOT_CONTEXT_KEY_AWAITING_IMAGE = "awaiting_image"

# --------------------------------------------------
# SECTION: Module identifiers
# [API_ID_<NAME>]

API_ID_STABILITY_AI = "stability.ai"
API_ID_LOCAL_PROCESSING = "server.machine"

# SECTION: Debounce settings
# [TIME_S_<NAME>]
TIME_S_WATCH_THROTTLE = 20
TIME_S_MSG_THROTTLE = 2