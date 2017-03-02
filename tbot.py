# -*-coding:utf-8-*-

import telebot
from telebot import types
import logging

logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename=u'mylog.log')

API_TOKEN = '327733244:AAGl7BmtE6MnnvJCdEH4cQ_0Ar4J-N2IfaM'

bot = telebot.TeleBot(API_TOKEN)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#    bot.reply_to(message, message.text)

def _send(chat_id, msg):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add('Расписание на сегодня', 'Расписание на завтра', 'Последние результаты')

    msg = bot.send_message(chat_id, '', reply_markup=markup)
    bot.register_next_step_handler(msg, process_step)


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    hello_test = 'Привет, %s! Я бот умеющий показывать расписание футбольных трансляций на ТВ и последние результаты матчей!' % message.from_user.first_name
    _send(message.chat.id, hello_test)


def process_step(message):
    chat_id = message.chat.id
    now = datetime.datetime.now()


    if message.text == 'Расписание на сегодня':
        file_path = './tdata/%s_translations' % date.strftime("%d-%m-%Y")
        my_file = open(file_path)
        f = my_file.read()
        _send(chat_id, f)

    if message.text == 'Расписание на завтра':
        date = date + datetime.timedelta(days=1)
        file_path = './tdata/%s_translations' % date.strftime("%d-%m-%Y")
        my_file = open(file_path)
        f = my_file.read()
        _send(chat_id, f)

    if message.text == 'Последние результаты':
        file_path_last_result = './tdata/last_result'
        my_file = open(file_path_last_result)
        f = my_file.read()
        _send(chat_id, f)


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception("polling error")

