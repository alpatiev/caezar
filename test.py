import sys
import constants
import random
import string
from entities import ChatCacheItem
from bot import BotModule
from logs import LogModule
from replies import PromptModule
from persistence import StorageModule

def test_database_0_block(storage):
    print("Running test_database_0_block...")
    result = storage.connect_database()
    if result is True:
        print("Connection established successfully.")
    else:
        print("Failed to establish connection:", result[1])
    print()

def test_database_1_block(storage):
    print("Running test_database_1_block...")
    result = storage.update_selected_id("suka blyat id")
    if result is True:
        print("Disconnected from the database.")
    else:
        print("No database connection to disconnect:", result[1])
    print()

def test_database_2_block(storage):
    print("Running test_database_2_block...")
    result = storage.fetch_selected_user("73185075")
    if result:
        print("Fetched user successfully:", result)
    else:
        print("Failed to fetch IDs:", result[1])
    print()

def test_database_3_block(storage):
    print("Running test_database_3_block...")
    test_id = "test_id"
    result = storage.update_selected_id(test_id)
    if result is True:
        print(f"Updated ID '{test_id}' successfully.")
    else:
        print(f"Failed to update ID '{test_id}':", result[1])
    print()

def test_database_4_block(storage):
    print("Running test_database_4_block...")
    test_id = "test_id"
    result = storage.delete_selected_id(test_id)
    if result is True:
        print(f"Deleted ID '{test_id}' successfully.")
    else:
        print(f"Failed to delete ID '{test_id}':", result[1])
    print()

def test_database_5_block(storage):
    print("Running test_database_5_block...")
    test_id = ''.join(random.choices(string.digits, k=8))
    test_item = ChatCacheItem(test_id, "/path/to/result.jpg", "text-to-image", "prompt text")
    result = storage.update_selected_user(test_item)
    if result is True:
        print(f"Updated user '{test_id}' successfully.")
    else:
        print(f"Failed to update user '{test_id}':", result[1])
    print()

def test():
    storage = StorageModule(constants.PATH_DATABASE)
    test_database_0_block(storage)
    test_database_1_block(storage)
    test_database_2_block(storage)
    test_database_3_block(storage)
    test_database_4_block(storage)
    test_database_5_block(storage)

if __name__ == "__main__":
    test()
