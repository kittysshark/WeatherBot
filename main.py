from pyowm import OWM
import telebot

bot = telebot.TeleBot("Your tg token")
owm = OWM('Your OWM token')
mgr = owm.weather_manager()

@bot.message_handler(commands=['start'])
def handle_start_help(message):
    bot.send_message(message.chat.id, "Привет!\nНапши мне свой город/страну и я скажу, какая там погода.")
pass

@bot.message_handler(content_types=['text'])
def send_welcome(message):
    try:
        text = message.text
        observation = mgr.weather_at_place(text)
        w = observation.weather
        if w.detailed_status == 'clear sky':
            clouds = 'Ясно☀️'
        elif w.detailed_status == 'broken clouds':
            clouds = 'Облачно с прояснениями🌥'
        elif w.detailed_status == 'overcast clouds':
            clouds = 'Облачно☁️'
        elif w.detailed_status == 'few clouds':
            clouds = 'Малооблачно🌤'
        elif w.detailed_status == 'haze':
            clouds = 'Туман🌫'


        weather = str(w.temperature('celsius')['temp']) + "°C  " + clouds
        humidity = str(w.humidity)
        wind = str(w.wind()['speed'])

        bot.send_message(message.chat.id, f'⛳️Погода в городе/стране {text}: \n🌡{weather}\n💧Влажность: {humidity}%\n🌬Ветер: {wind}м/с\n\nLink to chat: http://t.me/Tuiaio_bot')
    except Exception:
        bot.send_message(message.chat.id, 'Что-то не так! Проверь название города/страны.')


print("Bot Started!")
bot.infinity_polling()
