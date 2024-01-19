import data
from handlers.users.my import my_prompt_msg, weather_output_hourly, weather_output_daily
from loader import bot
from midwares.sql_lib import Hourly, Daily
from states.bot_states import States


@bot.callback_query_handler(
    func=lambda call: call.data
    in [f"{Hourly.table_name}_display", f"{Daily.table_name}_display"]
)
def set_weather_display(call):
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
def hourly_weather_prompt(call):
    bot.set_state(call.from_user.id, States.my_prompt, call.message.chat.id)
    my_prompt_msg(call.message)
