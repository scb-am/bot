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



headers = {'User-agent': 'Mozilla/5.0'}   #ссылка на форум
url = 'https://forum.militarist.ua/viewforum.php?f=183'
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')


loop = asyncio.get_event_loop()


types = telebot.types
bot = telebot.TeleBot(config.token)

#def func5():
    #if not hasattr(func5, '_state'):  # инициализация значения
        #func5._state = 0
    #print(func5._state)
    #func5._state = func5._state + 1

def func5():
    if not hasattr(func5, '_state'):  # инициализация значения
        func5._state = 0
    print('func do=', func5._state)
    if func5._state < 2:
        func5._state = func5._state + 1
    elif func5._state == 2:
        func5._state = func5._state - 1
    print('func posle=', func5._state)
       
func5()

#@bot.message_handler(commands=['whoisyourdaddy'])
#def any_msg(message):
#    print ('lalalo')


@bot.message_handler(content_types=["text"])
def any_msg(message):
    proverka = message.text
    print (proverka)
    if proverka == "/start" or proverka == "/whoisyourdaddy":
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Поиск ближайших игр", callback_data="test_by_date")
        callback_button2 = types.InlineKeyboardButton(text="Поиск игр по названию", callback_data="test_by_word")
        keyboard.add(callback_button, callback_button2)
        bot.send_message(message.chat.id, "Выбор способа поиска игр", reply_markup=keyboard)
    print ('hahahaha')
    start_time = 3
    print ('start=', start_time)
    if func5._state > 1:
        print ('kfkfkfkfk')
        func5()
        for number in range(20):
            text2 = soup.findAll('a', "topictitle")
            text3 = text2[number].get('href')
            text3 = text3[1:] 
            text3 = "https://forum.militarist.ua" + text3          #ссылка на страницу темы
            text2 = text2[number].getText()
            index = text2.find(message.text)
            #print (message.text)
            #message = call.message
            unix_timestamp = float(message.date)
            local_timezone = tzlocal.get_localzone() # get pytz timezone
            local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
            print(local_time.strftime("%m %d"))
            if index >= 0:
                print (text2)
                print (text3)  
                pagescr = urlopen(text3)
                soup2 = BeautifulSoup(pagescr, 'lxml')
                images = soup2.findAll('img')
                r_avtor = requests.get(text3, headers=headers)     #ищем автора первого поста
                soup_avtor = BeautifulSoup(r_avtor.text, 'lxml')
                text_avtor = soup_avtor.findAll('div', "postauthor")
                text_avtor = text_avtor[0].getText()
                print (text_avtor)
                nam = 100   #счетчик картинок
                for image in images:
                    textscr = image['alt']
                    index = textscr.find(u'Изображение')   #проход 1
                    #print index
                    if index >= 0:
                        if nam <101:
                            print(image['src'])
                            textscr2 = image['src']
                            print (textscr2)
                            print (nam)
                            nam += 1
                            #print (nam)
                    index2 = textscr.find(u'jpg')   #проход 2
                    #print index
                    if index2 >= 0:
                        if nam <101:
                            print(image['src'])
                            textscr2 = image['src']
                            textscr2 = textscr2[1:]
                            textscr2 = "https://forum.militarist.ua" + textscr2
                            print (textscr2)
                            print (nam)
                            nam += 1
                            #print (nam)
                text_avtor = u"Организатор - " + text_avtor   # добавляем к автору "организатор"
                keyboard = types.InlineKeyboardMarkup()
                url_button = types.InlineKeyboardButton(text2, text3)
                keyboard.add(url_button)
                bot.send_message(message.chat.id, text_avtor, reply_markup=keyboard)
                bot.send_photo(message.chat.id, textscr2)

  
  
# обработчик (кнопки вызывающие действия)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "test_by_date":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="по дате")
            #text = (message.text)
            #bot.send_message(message.chat.id, text)
            message = call.message
            unix_timestamp = float(message.date)
            local_timezone = tzlocal.get_localzone() # get pytz timezone
            local_time = datetime.fromtimestamp(unix_timestamp, local_timezone)
            print(local_time.strftime("%m %d"))
            text_year = 2018
            text_month = int(local_time.strftime("%m"))
            text_day = int(local_time.strftime("%d"))
            text_day_const = text_day
            text_date = calendar.weekday(text_year, text_month, text_day)  #определяем день недели
            razn = 6 - text_date   #определяем сколько дней осталось до конца недели
            text_month_long = calendar.monthrange(text_year, text_month)
            text_month_long = text_month_long[1]
            text_day = text_day - 1
            text_day_next_max = razn - text_month_long + text_day_const
            text_day_next = 0
            for day_namber in range(razn + 1):
                text_day = text_day + 1
                if text_day > text_month_long:
                    text_day_next = text_day_next + 1
                    text_month_next = text_month + 1
                    text_date = (text_day_next, text_month_next, text_year)
                    print (text_date)
                    text_find_1 = str(text_date[0])
                    text_find_2 = str(text_date[1])
                    text_find_3 = '2018'                        #обьявляем исключения для поиска
                    text_find_4 = '.18'
                    print (text_find_1)
                    print (text_find_2)
                    for number in range(20):
                        text_topic = soup.findAll('a', "topictitle")
                        text_url = text_topic[number].get('href')
                        text_url = text_url[1:] 
                        text_url = "https://forum.militarist.ua" + text_url          #ссылка на страницу темы
                        text_topic = text_topic[number].getText()
                        index = text_topic.find(text_find_1)
                        num_of_m = text_topic.count(text_find_1)     #количество совпадений номера месяца
                        num_of_y1 = text_topic.count(text_find_3)
                        num_of_y2 = text_topic.count(text_find_4)
                        index2 = text_topic.find(text_find_2)
                        if index >= 0 and index2 >= 0:
                            if num_of_m > num_of_y1:
                                if num_of_m > num_of_y2:
                                    print (text_topic)
                                    keyboard = types.InlineKeyboardMarkup()
                                    url_button = types.InlineKeyboardButton(text_topic, text_url)
                                    keyboard.add(url_button)
                                    bot.send_message(message.chat.id, 'text_avtor', reply_markup=keyboard)
                else:
                    text_date = (text_day, text_month, text_year)
                    print (text_date)
                    text_find_1 = str(text_date[0])
                    text_find_2 = str(text_date[1])
                    text_find_3 = '2018'                        #обьявляем исключения для поиска
                    text_find_4 = '.18'
                    for number in range(20):
                        text_topic = soup.findAll('a', "topictitle")
                        text_url = text_topic[number].get('href')
                        text_url = text_url[1:] 
                        text_url = "https://forum.militarist.ua" + text_url          #ссылка на страницу темы
                        text_topic = text_topic[number].getText()
                        index = text_topic.find(text_find_1)
                        num_of_m = text_topic.count(text_find_1)     #количество совпадений номера месяца
                        num_of_y1 = text_topic.count(text_find_3)
                        num_of_y2 = text_topic.count(text_find_4)
                        index2 = text_topic.find(text_find_2)
                        prov_date_1 = text_find_3.count(text_find_1)
                        prov_date_2 = text_find_4.count(text_find_1)
                        if index >= 0 and index2 >= 0:
                            if prov_date_1 == 0 and prov_date_2 == 0:
                                #if num_of_m > num_of_y1 and num_of_m > num_of_y2:
                                print (text_topic)
                                pagescr = urlopen(text_url)   #Ищем авторов и картинки
                                soup_img = BeautifulSoup(pagescr, 'lxml')
                                images = soup_img.findAll('img')
                                r_avtor = requests.get(text_url, headers=headers)     #ищем автора первого поста
                                soup_avtor = BeautifulSoup(r_avtor.text, 'lxml')
                                text_avtor = soup_avtor.findAll('div', "postauthor")
                                text_avtor = text_avtor[0].getText()
                                print (text_avtor)
                                nam = 100   #счетчик картинок
                                for image in images:
                                    textscr = image['alt']
                                    index = textscr.find(u'Изображение')   #проход 1
                                    #print index
                                    if index >= 0:
                                        if nam <101:
                                            print(image['src'])
                                            textscr2 = image['src']
                                            print (textscr2)
                                            print (nam)
                                            nam += 1
                                            #print (nam)
                                    index2 = textscr.find(u'jpg')   #проход 2
                                    #print index
                                    if index2 >= 0:
                                        if nam <101:
                                            print(image['src'])
                                            textscr2 = image['src']
                                            textscr2 = textscr2[1:]
                                            textscr2 = "https://forum.militarist.ua" + textscr2
                                            print (textscr2)
                                            print (nam)
                                            nam += 1
                                            #print (nam)
                                text_avtor = u"Организатор - " + text_avtor   # добавляем к автору "
                                keyboard = types.InlineKeyboardMarkup()
                                url_button = types.InlineKeyboardButton(text_topic, text_url)
                                keyboard.add(url_button)
                                bot.send_message(message.chat.id, text_avtor, reply_markup=keyboard)
                                bot.send_photo(message.chat.id, textscr2)
                            elif print (text_topic):
                                if num_of_m > num_of_y1 and num_of_m > num_of_y2:
                                    pagescr = urlopen(text_url)   #Ищем авторов и картинки
                                    soup_img = BeautifulSoup(pagescr, 'lxml')
                                    images = soup_img.findAll('img')
                                    r_avtor = requests.get(text_url, headers=headers)     #ищем автора первого поста
                                    soup_avtor = BeautifulSoup(r_avtor.text, 'lxml')
                                    text_avtor = soup_avtor.findAll('div', "postauthor")
                                    text_avtor = text_avtor[0].getText()
                                    print (text_avtor)
                                    nam = 100   #счетчик картинок
                                    for image in images:
                                        textscr = image['alt']
                                        index = textscr.find(u'Изображение')   #проход 1
                                        #print index
                                        if index >= 0:
                                            if nam <101:
                                                print(image['src'])
                                                textscr2 = image['src']
                                                print (textscr2)
                                                print (nam)
                                                nam += 1
                                                #print (nam)
                                        index2 = textscr.find(u'jpg')   #проход 2
                                        #print index
                                        if index2 >= 0:
                                            if nam <101:
                                                print(image['src'])
                                                textscr2 = image['src']
                                                textscr2 = textscr2[1:]
                                                textscr2 = "https://forum.militarist.ua" + textscr2
                                                print (textscr2)
                                                print (nam)
                                                nam += 1
                                                #print (nam)
                                    text_avtor = u"Организатор - " + text_avtor   # добавляем к автору "
                                    keyboard = types.InlineKeyboardMarkup()
                                    url_button = types.InlineKeyboardButton(text_topic, text_url)
                                    keyboard.add(url_button)
                                    bot.send_message(message.chat.id, text_avtor, reply_markup=keyboard)
                                    bot.send_photo(message.chat.id, textscr2)
        elif call.data == "test_by_word":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="по тексту")
            message = call.message
            bot.send_message(message.chat.id, 'введите поисковое слово')
            start_time = 20
            print ('start=', start_time)
            func5()
            


            
            

            
if __name__ == '__main__':
     bot.polling(none_stop=True)
