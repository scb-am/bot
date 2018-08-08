# -*- coding: utf-8 -*-
#python3.6


from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher
import keyboard as kb
import telebot
import config
from threading import Thread
import requests
import tzlocal
import asyncio
from bs4 import BeautifulSoup
from datetime import datetime   #для времени
from urllib.request import urlopen
import calendar
import codecs

from user_dialog import User_Dialog
from list_of_links import list_of_links
import day_x_date
global search_word #когда кнопка нажата то 1, до этого 0
global j  #определяем переменную счетчика по 5 игр
    


import time, threading  #модуль времени


filename = 'list_of_titles.txt' #файл с скачанной инфой
search_word = 0 #когда кнопка нажата то 1, до этого 0



types = telebot.types
bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    global search_word  #когда кнопка нажата то 1, до этого 0
    user_id = User_Dialog(message.chat.id, message.date, message.text)  #присваиваем переменной ай-ди юзера и дату сообщения
    user_id.print_massege()    #вызов класса
    user_id.keyboard()
    print('user_id = ', user_id.user_id)   #печатаем ай-ди юзера
    if search_word == 1:    #когда кнопка нажата то 1, до этого 0
        for i in range(35):  #перебор строк !!!!!!!!!!
            title = theme[i][0]
            title = title.lower()
            find_text = title.find(message.text.lower())
            if find_text >= 0:
                keyboard = types.InlineKeyboardMarkup(row_width=1) #вывод списка игр по поисковому слову
                url_button = types.InlineKeyboardButton(theme[i][0], theme[i][1])
                keyboard.add(url_button)
                headers = {'User-agent': 'Mozilla/5.0'}
                if str(theme[i][3]).rstrip() == '': #исключаем пустые картинки
                    #print('no jpg\n\n\n')
                    bot.send_message(message.chat.id, theme[i][0], reply_markup=keyboard)
                elif str(theme[i][3]).rstrip() == 'http://www1.ocn.ne.jp/~avro504/teppoo/icon/mp5.gif':
                    #print('tema Frola)))') #исключаем картинку Фрола
                    bot.send_message(message.chat.id, theme[i][0], reply_markup=keyboard)
                else:
                    response_img = requests.get(str(theme[i][3]).rstrip(), headers=headers)   #исключаем несуществующие картинки
                    response_img = str(response_img)
                    if response_img >= '<Response [404]>':
                        #print('bad URL\n\n\n')
                        bot.send_message(message.chat.id, theme[i][0], reply_markup=keyboard)
                    else:
                        bot.send_photo(message.chat.id, theme[i][3], reply_markup=keyboard)
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                callback_button = types.InlineKeyboardButton(text="Открыть короткое описание игры", callback_data=str(i))
                keyboard.add(callback_button)
                bot.send_message(message.chat.id, 'Организатор: ' + theme[i][2], reply_markup=keyboard)    
        search_word = 0
    
@bot.callback_query_handler(func=lambda call: True) #обработка нажатий кнопок
def callback_inline(call):
    global search_word  #когда кнопка нажата то 1, до этого 0
    global j  #определяем переменную счетчика по 5 игр
    #search_word = 1
    if call.message:
        if call.data == "test_by_date":     #при выборе поиска по дате
            #print('data')
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Список игр:')
            days_xs = day_x_date.day_x_date(call.message.date)#получаем массив
            for days_x in days_xs:
                #print(days_x)
                for i in range(35):  #перебор строк !!!!!!!!!
                    title = theme[i][0]
                    title = str(title)
                    #print(title) #
                    if days_x[0] == days_x[1]:
                        if days_x[1] < 10:
                            find_text = str(days_x[1])
                            find_text = '0' + find_text
                        else:
                            find_text = str(days_x[1])
                        num_of_month1 = '.' + find_text
                        num_of_month1 = title.count(num_of_month1)
                        #print('num_of_month1 = ', num_of_month1) #
                    else:
                        num_of_month1 = 0
                    if days_x[0] < 10:
                        find_text = str(days_x[0])
                        find_text = '0' + find_text
                    else:
                        find_text = str(days_x[0])
                    num_of_days = title.count(find_text)
                    #print('num_of_days= ', num_of_days)
                    if days_x[1] < 10:
                        find_text = str(days_x[1])
                        find_text = '0' + find_text
                    else:
                        find_text = str(days_x[1])
                    num_of_month = title.count(find_text)
                    #print('num_of_month= ', num_of_month)
                    num_of_year1 = title.count('2018')
                    num_of_year2 = title.count('.18')
                    num_of_year3 = title.count('201')
                    num_of_year4 = title.count('2088')
                    if num_of_days > 0 and num_of_month > 0:
                        if num_of_days > (num_of_month1 + num_of_year4):
                            #print('!!!!!!!!!!!!!! title = ', theme[i][0])
                            keyboard = types.InlineKeyboardMarkup(row_width=1) #вывод списка игр по дате
                            url_button = types.InlineKeyboardButton(theme[i][0], theme[i][1])
                            keyboard.add(url_button)
                            headers = {'User-agent': 'Mozilla/5.0'}
                            if str(theme[i][3]).rstrip() == '': #исключаем пустые картинки
                                #print('no jpg\n\n\n')
                                bot.send_message(call.message.chat.id, theme[i][0], reply_markup=keyboard)
                            elif str(theme[i][3]).rstrip() == 'http://www1.ocn.ne.jp/~avro504/teppoo/icon/mp5.gif':
                                #print('tema Frola)))') #исключаем картинку Фрола
                                bot.send_message(call.message.chat.id, theme[i][0], reply_markup=keyboard)
                            else:
                                response_img = requests.get(str(theme[i][3]).rstrip(), headers=headers)   #исключаем несуществующие картинки
                                response_img = str(response_img)
                                if response_img >= '<Response [404]>':
                                    #print('bad URL\n\n\n')
                                    bot.send_message(call.message.chat.id, theme[i][0], reply_markup=keyboard)
                                else:
                                    bot.send_photo(call.message.chat.id, theme[i][3], reply_markup=keyboard)
                            keyboard = types.InlineKeyboardMarkup(row_width=1)
                            callback_button = types.InlineKeyboardButton(text="Открыть короткое описание игры", callback_data=str(i))
                            keyboard.add(callback_button)
                            bot.send_message(call.message.chat.id, 'Организатор: ' + theme[i][2], reply_markup=keyboard)
                    
                    
                
                #for day_x in days_x:
                    #print(day_x)
            
        elif call.data == "test_by_word":   #при выборе поиска по слову
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите фрагмент названия для поиска')
            search_word = 1  #когда кнопка нажата то 1, до этого 0
        elif call.data == "all_games":  #при выборе всех игр
            j = 1
            theme_reply_5(j, call)
        elif call.data == "Next_5":  #при выборе следующих 5
            if j <= 6:
                j = j + 1
                theme_reply_5(j, call)
            else:
                bot.send_message(call.message.chat.id, 'Конец списка')
                
        else:
            i = int(call.data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=theme[i][0] + theme[i][4])
            
                
                
               
                

@bot.message_handler(content_types=["contact"])     #отлавливаем айди пользователей которыми поделились
def cotact_user_id(message):
    print(message.contact.user_id)
    #bot.send_message(message.contact.user_id, 'бибика)')
    #bot.send_photo(message.contact.user_id, 'https://www.e-xecutive.ru/uploads/article/image/1985759/thumb_europlan_exe_car.jpg')


def theme_reply_5(j, call):  #вывод тем по 5 шт
    reset_messege = 0
    start_j = (j-1)*5
    end_j = (j-1)*5+6
    for i in range(start_j, end_j):  #перебор строк !!!!!!!!!!
        if i <= (start_j+4):
            keyboard = types.InlineKeyboardMarkup(row_width=1)  #вывод списка игр
            url_button = types.InlineKeyboardButton(theme[i][0], theme[i][1])
            keyboard.add(url_button)
            headers = {'User-agent': 'Mozilla/5.0'}
            if str(theme[i][3]).rstrip() == '': #исключаем пустые картинки
                #print('no jpg\n\n\n')
                bot.send_message(call.message.chat.id, theme[i][0], reply_markup=keyboard)
            elif str(theme[i][3]).rstrip() == 'http://www1.ocn.ne.jp/~avro504/teppoo/icon/mp5.gif':
                #print('tema Frola)))') #исключаем картинку Фрола
                bot.send_message(call.message.chat.id, theme[i][0], reply_markup=keyboard)
            else:
                response_img = requests.get(str(theme[i][3]).rstrip(), headers=headers)   #исключаем несуществующие картинки
                response_img = str(response_img)
                if response_img >= '<Response [404]>':
                    #print('bad URL\n\n\n')
                    bot.send_message(call.message.chat.id, theme[i][0], reply_markup=keyboard)
                else:
                    bot.send_photo(call.message.chat.id, theme[i][3], reply_markup=keyboard)
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            callback_button = types.InlineKeyboardButton(text="Открыть короткое описание игры", callback_data=str(i))
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, 'Организатор: ' + theme[i][2], reply_markup=keyboard)
        else:
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            callback_button = types.InlineKeyboardButton(text="Next", callback_data="Next_5")
            keyboard.add(callback_button)
            bot.send_message(call.message.chat.id, 'Следующие 5 игр', reply_markup=keyboard)

    
    
def parce_forum():  #парсинг форума каждые _ секунд
    global theme  #определяем глобальную переменную
    with open(filename, 'w') as file_object:   #вызов функции для записи в файл
        list_of_links(file_object)
    threading.Timer(600, parce_forum).start()
    with open(filename) as file_object: #чтение текстового файла
        text_lines = file_object.readlines()
        num_of_lines = 0
        num_of_blocks = 1
        n = 36  #создание списка, n число строк !!!!!!
        m = 6  #создание списка, m число столбцов
        theme = [0] * n  #заполнение списка нулями
        for i in range(n):
            theme[i] = [0] * m
        for text_line in text_lines:    #заполнение списка строками файла
            num_of_lines = num_of_lines + 1
            num_of_info = num_of_lines - (num_of_blocks - 1) * 6
            theme[int(num_of_blocks-1)][int(num_of_info-1)] = text_line[:3000]
            #print(theme[int(num_of_blocks-1)][int(num_of_info-1)])
            if num_of_lines % 6 == 0:
                num_of_blocks = num_of_blocks + 1
        #print(text_lines[3])
parce_forum()

        

            
if __name__ == '__main__':
     bot.polling(none_stop=True)
