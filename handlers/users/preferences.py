from telebot import types
from telebot.types import InlineKeyboardMarkup, Message

import data
from keyboards.inline.inline_buttons import (
    inline_current_settings_btn,
    inline_daily_settings_btn,
    inline_cancel_btn,
    inline_hourly_settings_btn,
    inline_change_settings_btn,
    inline_save_settings_btn,
    inline_exit_btn,
)
from loader import bot
from midwares.sql_lib import Current, Hourly, Daily
from states.bot_states import States


@bot.message_handler(commands=["prefs"])
@bot.message_handler(state=States.customize_prompt)
def preferences_prompt(message) -> None:
    """
    Function. Executing prefs command and display prefs prompt message with inline button keyboard.
    :param message:
    :return: None
    """

    bot.set_state(message.from_user.id, States.customize_prompt, message.chat.id)

    markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    markup.add(
        inline_current_settings_btn(),
        inline_hourly_settings_btn(),
        inline_daily_settings_btn(),
    )
    markup.add(inline_cancel_btn())

    msg: Message = bot.send_message(
        message.chat.id, "Customize your weather display:", reply_markup=markup
    )
    data.globals.users_dict[message.from_user.id]["message_id"] = msg.message_id


@bot.message_handler(state=States.customize_current)
def customize_current_setting(message) -> None:
    """
    Function. Change current weather user setting (on/off).
    :param message:
    :return: None
    """
    user_id: int = States.customize_current.user_id
    chat_id: int = message.chat.id

    setting = Current.table_name
    settings_change_output(
        user_id, chat_id, States.customize_current.settings_dict, setting
    )


@bot.message_handler(state=States.customize_hourly)
def customize_hourly_setting(message) -> None:
    """
    Function. Change hour weather user setting.
    :param message:
    :return: None
    """
    user_id: int = States.customize_hourly.user_id
    chat_id: int = message.chat.id

    setting = Hourly.table_name
    settings_change_output(
        user_id, chat_id, States.customize_hourly.settings_dict, setting
    )


@bot.message_handler(state=States.customize_daily)
def customize_daily_setting(message) -> None:
    """
    Function. Change day weather user setting.
    :param message:
    :return: None
    """
    user_id: int = States.customize_daily.user_id
    chat_id: int = message.chat.id

    setting: str = Daily.table_name
    settings_change_output(
        user_id, chat_id, States.customize_daily.settings_dict, setting
    )


@bot.message_handler(state=States.change_setting)
def change_settings(message) -> None:
    """
    Function. Changing user settings.
    :param message:
    :return: None
    """
    set_dict_for_changes: dict = {}
    user_id: int = States.change_setting.user_id
    match States.change_setting.setting:
        case Current.table_name:
            set_dict_for_changes = States.customize_current.settings_dict
        case Hourly.table_name:
            set_dict_for_changes = States.customize_hourly.settings_dict
        case Daily.table_name:
            set_dict_for_changes = States.customize_daily.settings_dict

    markup = types.InlineKeyboardMarkup()
    for row in set_dict_for_changes:
        for setting, isSet in row.items():
            setting_field = setting
            if "_" in setting:
                setting = setting.replace("_", " (") + ")"
            markup.row(
                types.InlineKeyboardButton(
                    f"{setting.upper()}: {'yes' if isSet else 'no'}",
                    callback_data=f"Switch setting|{States.change_setting.setting}|{setting_field}",
                )
            )
    markup.row(inline_save_settings_btn(States.change_setting.setting))
    markup.row(inline_exit_btn())

    msg: Message = bot.send_message(
        message.chat.id, "Tap to change setting:", reply_markup=markup
    )
    if not data.globals.users_dict[user_id]["message_id"] == 0:
        bot.edit_message_reply_markup(
            message.chat.id,
            message_id=data.globals.users_dict[user_id]["message_id"],
            reply_markup="",
        )
    data.globals.users_dict[user_id]["message_id"] = msg.message_id


def settings_change_output(
    user_id: int, chat_id: int, user_settings_dict: list, setting: str
) -> None:
    """
    Function. Display user settings message.
    :param user_id:
    :param chat_id:
    :param user_settings_dict: user setting dict
    :param setting: setting to change (current, daily, current)
    :return: None
    """
    markup: InlineKeyboardMarkup = types.InlineKeyboardMarkup()
    markup.add(inline_change_settings_btn(setting), inline_cancel_btn())
    settings: str = "\U0001F4C3  <b>Advanced settings:</b>\n"
    settings = create_output_msg(user_settings_dict, settings)
    msg: Message = bot.send_message(
        chat_id, settings, parse_mode="HTML", reply_markup=markup
    )
    bot.edit_message_reply_markup(
        chat_id,
        message_id=data.globals.users_dict[user_id]["message_id"],
        reply_markup="",
    )
    data.globals.users_dict[user_id]["message_id"] = msg.message_id


def create_output_msg(user_settings: list, settings: str) -> str:
    """
    Function. User settings msg string.
    :param user_settings:
    :param settings:
    :return: None
    """
    for row in user_settings:
        for k, v in row.items():
            if "_" in k:
                k = k.replace("_", " (") + ")"
            if v == 0:
                settings += f"      - {k}: <b>no</b>\n"
                continue
            settings += f"      - {k}: <b>yes</b>\n"
    return settings
