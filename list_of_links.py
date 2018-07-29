# -*- coding: utf-8 -*-
#python3.6

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup



headers = {'User-agent': 'Mozilla/5.0'}   
url = 'https://forum.militarist.ua/viewforum.php?f=183' #ссылка на форум
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')

filename = 'list_of_titles.txt'


def list_of_links(file_object):
    num_of_titles = 0
    for number in range(40):    #количество тем = 54
        if num_of_titles < 5:
            num_of_titles = num_of_titles + 1
        else:
            list_of_topics = soup.findAll('a', "topictitle")    #парсим по topictitle
            link_of_topic = list_of_topics[number].get('href')  #определяем ссылку темы
            link_of_topic = link_of_topic[1:]   #срезаем лишний символ
            link_of_topic = "https://forum.militarist.ua" + link_of_topic          #ссылка на страницу темы
            name_of_topic = list_of_topics[number].getText()    #забираем текст названия темы
            #print('topic - ', name_of_topic)
            file_object.write(name_of_topic)
            file_object.write('\n')
            #print('link - ', link_of_topic)
            file_object.write(link_of_topic)
            file_object.write('\n')
            #index = text2.find(message.text)
            page_topic = requests.get(link_of_topic, headers=headers)
            soup_page_topic = BeautifulSoup(page_topic.text, 'lxml')
            avtor_topic = soup_page_topic.findAll('div', "postauthor")     #ищем автора
            avtor_topic = avtor_topic[0].getText()
            #print('autor - ', avtor_topic, '\n')
            file_object.write(avtor_topic)
            file_object.write('\n')
            images_of_topic = soup_page_topic.findAll('img') #ищем картинки
            nam = 100   #счетчик картинок
            link_of_img_final = ''
            for image_of_topic in images_of_topic:
                link_of_img = image_of_topic['alt']
                index = link_of_img.find(u'Изображение')   #проход 1
                if index >= 0:
                    if nam <101:
                        link_of_img_final = image_of_topic['src']
                        nam += 1
                index2 = link_of_img.find(u'jpg')   #проход 2
                if index2 >= 0:
                    if nam <101:
                        link_of_img_final = image_of_topic['src']
                        link_of_img_final = link_of_img_final[1:]
                        link_of_img_final = "https://forum.militarist.ua" + link_of_img_final
                        nam += 1
            #print('image - ',link_of_img_final, '\n\n')
            file_object.write(link_of_img_final)
            file_object.write('\n')
            texts_topic = soup_page_topic.findAll('div', "postbody")     #ищем сообщения
            #for text_topic in texts_topic:
                #text_topic = text_topic.getText()
                #print('text - ', text_topic, '\n')
            texts_topic = texts_topic[0].getText()
            text_topic_global = ''
            for text_topic in texts_topic:
                text_topic_global += text_topic.rstrip('\n\n')
            #print('text - ', text_topic_global, '\n')
            file_object.write(text_topic_global)
            file_object.write('\n\n')
            num_of_titles = num_of_titles + 1

 
            
with open(filename, 'w') as file_object:
    list_of_links(file_object)
