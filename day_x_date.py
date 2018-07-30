# -*- coding: utf-8 -*-
#python3.6

import tzlocal #дата/время
from datetime import datetime #для времени
import calendar #для времени



def day_x_date(message_date):   #получаем переменную дату сообщения
    local_timezone = tzlocal.get_localzone()
    local_time = datetime.fromtimestamp(message_date, local_timezone) #подключаем модуль даты
    #print(local_time.strftime("%m %d")) #формат даты
    text_year = int(local_time.strftime("%y"))
    text_month = int(local_time.strftime("%m"))
    text_day = int(local_time.strftime("%d"))
    #text_day = 30
    text_day_const = text_day
    text_date = calendar.weekday(text_year, text_month, text_day)  #определяем день недели
    razn = 6 - text_date   #определяем сколько дней осталось до конца недели
    text_month_long = calendar.monthrange(text_year, text_month)    #определяем последнее число месяца
    text_month_long = text_month_long[1]    #определяем последнее число месяца
    text_day = text_day - 1  #необходимо для счетчика цикла 111
    text_day_next_max = razn - text_month_long + text_day_const
    text_day_next = 0
    text_date_list = [] #создаем пустой список
    for day_namber in range(razn + 1):
            text_day = text_day + 1  #счетчик 111
            if text_day > text_month_long:
                text_day_next = text_day_next + 1
                text_month_next = text_month + 1
                text_date = (text_day_next, text_month_next, text_year) #присваиваем кортежу дату
                text_date_list.append(text_date)    #добавляем кортеж в список
            else:
                text_date = (text_day, text_month, text_year)   #присваиваем кортежу дату
                text_date_list.append(text_date)    #добавляем кортеж в список
    return text_date_list #возвращаем список дат
