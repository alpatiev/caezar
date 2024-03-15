# --------------------------------------------------
# NOTE: SQL chat entity
# Stored betweed sessions, mapped to DB_TABLE_KEY_ID_LIST
#
class ChatCacheItem:
    def __init__(self, id, image_path, pipeline, prompt):
        self.id = id
        self.image_path = image_path
        self.pipeline = pipeline
        self.prompt = prompt
