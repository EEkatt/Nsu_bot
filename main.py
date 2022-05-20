import telebot
import requests
import datetime
from telebot import types
from bs4 import BeautifulSoup as BS
import pandas as pd
from tabulate import tabulate



bot = telebot.TeleBot("5335300808:AAEovT8qvpTn4CQivU0N58zGDboGN2cy-pA")

r = requests.get('https://table.nsu.ru/faculties#call-schedule')
html = BS(r.content, 'html.parser')


day = datetime.datetime.today().isoweekday()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
    item1 = types.KeyboardButton('Расписание занятий')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Здравствуйте, {0.first_name} :) '.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types= ['text'])
def bot_message(message):
    if message.text == 'Расписание занятий':
        if day == 7: bot.send_message(message.chat.id, "Сегодня выходной. Занятий нет")
        else:
            msg1 = bot.send_message(message.chat.id, "Введите номер группы")
            bot.register_next_step_handler(msg1, today_time)
    else:
        bot.send_message(message.chat.id, "УТОЧНИТЕ ЗАПРОС\nЯ вас не понимаю\n")


@bot.message_handler(content_types= ['text'])
def today_time(message):
    url = "https://table.nsu.ru/group/" + str(message.text)
    time_table = requests.get(url)
    if time_table.status_code == 200:
        dfs = pd.read_html(url)
        week_day = dfs[1].columns[day]
        cur_table = dfs[1][['Время', week_day]].fillna('-').set_index('Время')
        bot.send_message(message.chat.id, tabulate(cur_table, headers = 'keys'))

    else:
        msg2 = bot.send_message(message.chat.id, "Такой группы не существует. Введите номер группы")
        bot.register_next_step_handler(msg2, today_time)
bot.polling(none_stop= True)


