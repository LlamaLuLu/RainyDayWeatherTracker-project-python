import requests
import os

# open weather forecast
api_key = os.environ.get("API_KEY")

# telegram bot
bot_name = "LlamaLuLuBot"
http_access_token = os.environ.get("HTTP_ACCESS_TOKEN")
bot_chatID = os.environ.get("BOT_CHATID")

co_ords = [
    (-34.099572, 18.485757, "L's home🏡"),
    (-33.955599, 18.464269, "uni🏫"),  
    (35.088468, 138.960194, "M's house🌸")
]

def telegram_bot_send_msg(bot_message):
    telegram_params = {
        "chat_id": bot_chatID,
        "parse_mode": "Markdown",
        "text": bot_message
    }
    telegram_api_url = "https://api.telegram.org/bot" + http_access_token + "/sendMessage"

    response = requests.get(telegram_api_url, params=telegram_params)
    return response.json()


def msg_creator(loc_list):
    """returns message to send to phone"""
    # when at least 1 element exists in list
    locations_txt = ""
    for loc in loc_list:
        if loc_list.index(loc) == 0:
            locations_txt += loc
        else:
            if loc_list.index(loc) == (len(loc_list) - 1):
                locations_txt += f" and {loc}"
            else:
                locations_txt += f", {loc}"
    msg = f"Bring an umbrella!☂️🌧️\nIt's going to rain at {locations_txt}"
    return msg


def rain_check(lat, long, location):
    """returns list of rainy locations from existing co-ords"""
    global rainy_locations_list
    params = {
        "lat": lat,
        "lon": long,
        "appid": api_key,
        "cnt": 4
    }

    # needs to be url :. include https
    response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params=params)
    response.raise_for_status()
    weather_data = response.json()

    will_rain = False

    for hour_data in weather_data["list"]:
        condition_code = hour_data["weather"][0]["id"]
        if int(condition_code) < 700:
            will_rain = True

    if will_rain:
        rainy_locations_list.append(location)


rainy_locations_list = []
for i in co_ords:
    i_lat, i_long, i_name = i
    rain_check(i_lat, i_long, i_name)
# print(rainy_locations_list)

if len(rainy_locations_list) > 0:
    send_txt = telegram_bot_send_msg(msg_creator(rainy_locations_list))
    # print(send_txt)
    print("Message successfully sent.")
