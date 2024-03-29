from telebot import types

import data
from handlers.users.my import my_prompt_msg
from keyboards.inline.inline_buttons import inline_set_wishlist_btn, inline_cancel_btn
from keyboards.reply.reply_buttons import reply_bottom_menu_kb
from loader import bot
from midwares.db_conn_center import write_data, read_data, read_data_row
from midwares.sql_lib import Wishlist, User
from states.bot_states import States
from utils.global_functions import delete_msg


@bot.callback_query_handler(func=lambda call: call.data == "Clear wishlist")
def clear_wishlist(call) -> None:
    """
    Function. Clearing wishlist.
    :param call:
    :return:
    """
    query = (
        f"DELETE FROM {Wishlist.table_name} "
        f"WHERE {Wishlist.wishlist_user_id}="
        f"({User.get_user_id(call.from_user.id)})"
    )
    write_data(query)
    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup="",
    )

    bot.send_message(
        call.message.chat.id, "\U00002705 Your wishlist is empty now! /add location ?"
    )
    bot.delete_state(call.from_user.id, call.message.chat.id)
    data.globals.users_dict[call.from_user.id]["message_id"] = 0

    keyboards = reply_bottom_menu_kb(call.from_user.id)
    bot.send_message(
        call.message.chat.id,
        "Your bottom menu updated!",
        reply_markup=keyboards,
    )


@bot.callback_query_handler(func=lambda call: call.data == "Change wishlist")
def change_wishlist(call) -> None:
    """
    Function. Changing wishlist content.
    :param call:
    :return:
    """
    for loc, isSet in States.change_wishlist.wishlist.items():
        if not isSet:
            query: str = (
                f"DELETE FROM {Wishlist.table_name} "
                f"WHERE {Wishlist.name}='{loc}' "
                f"AND {Wishlist.wishlist_user_id}="
                f"({User.get_user_id(call.from_user.id)})"
            )
            write_data(query)

    bot.delete_state(call.from_user.id, call.message.chat.id)
    delete_msg(call.message.chat.id, call.from_user.id)

    query: str = (
        f"SELECT {Wishlist.name} "
        f"FROM {Wishlist.table_name} "
        f"WHERE {Wishlist.wishlist_user_id}="
        f"({User.get_user_id(call.from_user.id)})"
    )

    get_user_wishlist = read_data(query)

    if not get_user_wishlist:
        bot.send_message(
            call.message.chat.id, "Your wishlist is empty now! /add location!"
        )
    else:
        bot.send_message(call.message.chat.id, "New /wishlist was set!")
    data.globals.users_dict[call.from_user.id]["message_id"] = 0


@bot.callback_query_handler(func=lambda call: "Remove" in call.data)
def remove_from_wishlist(call) -> None:
    """
    Function. Removing item from wishlist (created class dict) while in change_wishlist state.
    :param call:
    :return:
    """
    parse_call_data = call.data.split("|")
    States.change_wishlist.wishlist[parse_call_data[1]] = False
    markup = types.InlineKeyboardMarkup()
    for loc, isSet in States.change_wishlist.wishlist.items():
        if isSet:
            markup.add(
                types.InlineKeyboardButton(f"{loc}", callback_data=f"Remove|{loc}")
            )
    markup.row(inline_set_wishlist_btn())
    markup.row(inline_cancel_btn())

    bot.edit_message_reply_markup(
        call.message.chat.id,
        message_id=data.globals.users_dict[call.from_user.id]["message_id"],
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: "Wishlist output" in call.data)
def wishlist_loc_output(call) -> None:
    """
    Function. Wishlist location display (call 'my' command).
    :param call:
    :return:
    """
    States.my_prompt.user_id = call.from_user.id
    parse_callback = call.data.split("|")
    States.my_prompt.loc_name = parse_callback[1]

    query: str = (
        f"SELECT {Wishlist.id} "
        f"FROM {Wishlist.table_name} "
        f"WHERE {Wishlist.wishlist_user_id}="
        f"({User.get_user_id(call.from_user.id)}) "
        f"AND {Wishlist.name}='{parse_callback[1]}'"
    )

    States.my_prompt.loc_id = read_data(query)[0][0]

    my_prompt_msg(call.message)
