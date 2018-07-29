# -*- coding: utf-8 -*-
#python3.6


import telebot
import day_x_date
import config #токкен

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton     #клавиатура
import keyboard as kb

from datetime import datetime   #для времени


types = telebot.types
bot = telebot.TeleBot(config.token)


class User_Dialog():
    def __init__(self, user_id, message_date, message_text):
        self.user_id = user_id
        self.message_date = day_x_date.day_x_date(message_date) #получаем массив дат
        self.message_text = message_text

    def print_massege(self):
        print(self.message_date)

    def keyboard(self):
        if self.message_text == "/start" or self.message_text == "/111":    #если команда то вывести клавиатуру
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            callback_button = types.InlineKeyboardButton(text="Все игры", callback_data="all_games")
            callback_button2 = types.InlineKeyboardButton(text="Поиск ближайших игр", callback_data="test_by_date")
            callback_button3 = types.InlineKeyboardButton(text="Поиск игр по названию", callback_data="test_by_word")
            keyboard.add(callback_button, callback_button2, callback_button3)
            bot.send_message(self.user_id, "Выбор способа поиска игр", reply_markup=keyboard)
