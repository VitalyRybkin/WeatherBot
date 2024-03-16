import data
from handlers.users.my import my_prompt_msg, weather_output_hourly, weather_output_daily
from loader import bot
from midwares.api_conn_center import get_current_weather, get_daily_forecast_weather
from midwares.db_conn_center import read_data_row
from midwares.sql_lib import Hourly, Daily, Current, User
from states.bot_states import States
from utils.global_functions import edit_reply_msg


@bot.callback_query_handler(
    func=lambda call: call.data
    in [f"{Hourly.table_name}_display", f"{Daily.table_name}_display"]
)
def set_weather_display(call) -> None:
    """
    Function. Setting next state.
    :param call:
    :return:
    """
    if call.data == f"{Hourly.table_name}_display":
        bot.set_state(
            call.from_user.id, States.weather_display_hourly, call.message.chat.id
        )
        States.weather_display_hourly.user_id = call.from_user.id

        data.globals.users_dict[call.from_user.id]["state"] = bot.get_state(
            call.from_user.id, call.message.chat.id
        )
        weather_output_hourly(call.message)

    if call.data == f"{Daily.table_name}_display":
        bot.set_state(
            call.from_user.id, States.weather_display_daily, call.message.chat.id
        )
        States.weather_display_daily.user_id = call.from_user.id

        data.globals.users_dict[call.from_user.id]["state"] = bot.get_state(
            call.from_user.id, call.message.chat.id
        )
        weather_output_daily(call.message)


@bot.callback_query_handler(func=lambda call: call.data == "back_to_weather_prompt")
def hourly_weather_prompt(call) -> None:
    """
    Function. Setting previous state.
    :param call:
    :return:
    """
    bot.set_state(call.from_user.id, States.my_prompt, call.message.chat.id)
    my_prompt_msg(call.message)


@bot.callback_query_handler(
    func=lambda call: call.data == f"{Current.table_name}_display"
)
def display_current_weather(call):
    bot.delete_state(call.from_user.id, call.message.chat.id)
    current_weather_pic = get_current_weather(
        States.my_prompt.loc_id, call.from_user.id
    )
    edit_reply_msg(call.message.chat.id, call.from_user.id)
    with open(current_weather_pic, "rb") as p:
        bot.send_photo(call.message.chat.id, p)
    data.globals.users_dict[call.from_user.id]["message_id"] = 0


@bot.callback_query_handler(func=lambda call: f"{Daily.table_name}|day|" in call.data)
def display_daily_weather(call):
    query = User.get_user_location_info(bot_user_id=call.from_user.id)
    loc_id = read_data_row(query)[0]
    parsed_call_data = call.data.split("|")
    forecast_weather_pic = get_daily_forecast_weather(
        loc_id["id"], call.from_user.id, parsed_call_data[2]
    )
    with open(forecast_weather_pic, "rb") as p:
        bot.send_photo(call.message.chat.id, p)
    data.globals.users_dict[call.from_user.id]["message_id"] = 0
