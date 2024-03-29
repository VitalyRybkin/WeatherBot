import atexit
import copy
import json

import signal
import sqlite3

from telebot import custom_filters

from handlers.call_backs import (
    user_config_callback,
    default_config_callback,
    default_callback,
    add_location_callback,
    wishlist_callback,
    settings_callback,
)
from loader import bot
from handlers.users import (
    start,
    my,
    help,
    set_location,
    empty,
    add_location,
    change,
    preferences,
    wishlist,
    user_config,
    default_config,
    commands_handling, glance,
)
from utils.notifications import admin_notify, stopped
from utils.bot_commands import set_menu_commands
from data import config
import os
import data.globals

bot.register_message_handler(start)
bot.register_message_handler(my)
bot.register_message_handler(help)
bot.register_message_handler(set_location)
bot.register_message_handler(empty)
bot.register_message_handler(add_location)
bot.register_message_handler(change)
bot.register_message_handler(preferences)
bot.register_message_handler(wishlist)
bot.register_message_handler(user_config)
bot.register_message_handler(default_config)
bot.register_message_handler(user_config_callback)
bot.register_message_handler(default_config_callback)
bot.register_message_handler(default_callback)
bot.register_message_handler(add_location_callback)
bot.register_message_handler(wishlist_callback)
bot.register_message_handler(settings_callback)
bot.register_message_handler(glance)
bot.register_message_handler(commands_handling)


if __name__ == "__main__":
    print("Bot has started!")
    admin_notify()
    set_menu_commands(bot)

    DATABASE = config.DB

    def handler(signum, frame):
        # with open('./data/settings.pkl', 'wb') as file:
        #     print("Signal Number:", signum, " Frame: ", frame)
        #     pickle.dump(data.globals.users_dict, file)
        stopped()
        with open("./data/user_dict.json", "w") as write_dict:
            json.dump(data.globals.users_dict, write_dict, indent=4)
            print("Signal Number:", signum, " Frame: ", frame)
        os.kill(os.getpid(), 9)

    atexit.register(handler)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    if os.path.exists("./data/user_dict.json"):
        # with open('settings.pkl', 'rb') as f:
        #     data.globals.users_dict = pickle.load(f)
        with open("./data/user_dict.json", "r") as read_dict:
            json_dict = json.load(read_dict)
        new_dict = {}
        for k, v in json_dict.items():
            new_dict[int(k)] = v
            if not v["message_id"] == 0:
                bot.delete_message(v["chat_id"], v["message_id"])
                v["message_id"] = 0
            if v["message_list"]:
                for msg in v["message_list"]:
                    bot.delete_message(v["chat_id"], msg)
                v["message_list"].clear()
        data.globals.users_dict = copy.deepcopy(new_dict)

    if not os.path.exists(f"./data/{DATABASE}"):
        with sqlite3.connect(f"./data/{DATABASE}") as connection:
            cursor = connection.cursor()
            cursor.executescript(open("./data/schema.sql", "r").read())
            connection.commit()
            cursor.close()

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
