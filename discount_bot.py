__author__ = 'Alex Bulavin'
'''
Это только рабочий пример для изучения с нуля. Это не производство!!!
Даже не соответствует стандарту PEP8
Так что нужно рефакторить
Но снимает преграды и непонимание для новичков

This is just a working example to learn from scratch. This is not production!
Not even PEP8 compliant
So you need to refactor
But breaks down barriers and misunderstandings for beginners
'''
from aiogram import Bot, Dispatcher, executor, types
import os
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
from main import collect_data
import json
import pandas as pd
import requests
from datetime import datetime
from pythonping import ping
import time
import locale

# Создаём data frame
df_sites = pd.read_csv('/Users/alex/Documents/Python_projects/Dynamic_site_parser_and_telegram_bot/monitored_urls.csv')
print(df_sites, '\nLine 15')
#    df_logs = pd.read_csv('/Users/alex/Documents/Python_projects/website_monitor/sites_monitoing_log.csv')

# Done! Congratulations on your new bot. You will find it at t.me/SalomonParser_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.
#
# Use this token to access the HTTP API:
# 2052937653:AAGgdW******************* #Заменить на свой токен
# Keep your token secure and store it safely, it can be used by anyone to control your bot.
#
# For a description of the Bot API, see this page: https://core.telegram.org/bots/api

#Создаём бота в Телеграм и получаем его токен
bot = Bot(token='2052937653:AAGgdW*******************', parse_mode=types.ParseMode.HTML)
#Подробнее здесь: https://boto.agency/blog/kak-polychit-api-token-telegram/
userid = '@S**********_bot' # Задаём имя своего бота
#bot = Bot(token=os.getenv('TOKEN'))

#Создаём диспетчера
dp = Dispatcher(bot)
print(locale.getlocale(category=locale.LC_ALL))
locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))#

def send_message(message):

    """
    Посылаем сообщение пользователю
    """

    bot.send_message(userid, message, parse_mode='HTML', disable_web_page_preview=True)
    print('I am in send_message(message)')

#Создаём простую функцию ответа на команду и протестируем её
@dp.message_handler(commands='start')
async def start(message: types.Message):
    #Объединяем несколько кнопок в список для работы с клавиатурой
    # start_buttons = ["Кроссовки", "Мониторинг сайтов", "Крупа"]
    start_buttons = ["Мониторинг сайтов"]
    #Создаём объект клавиатуры
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Привет! Как дела? Проверяю сайты..', reply_markup=keyboard)
    time.sleep(2)
    while True:
#Запускаем бесконечный цикл.
        if datetime.now().strftime("%H:%M") == "09:00:00": #Раз в сутки подтверждаем пользователю, что бот жив и сервис жив.

            await message.answer("Hi Boss, I am alive!")

        for index, website in df_sites.iterrows():

            try:
                response = requests.get(
                    website[0])  # Делаем запрос к нужному сайту и сохраняем данные в переменную response
                # print(website[0], " is ", response.status_code)
                if response.status_code == 200:  # Форматирование https://docs-python.ru/standart-library/modul-datetime-python/kody-formatirovanija-strftime-strptime-modulja-datetime/
                    result = f'{datetime.now().strftime("%d %B %Y %H:%M:%S")}\n' \
                             f'{website[0]} ' \
                             'OK'
                else:
                    result = f'{datetime.now().strftime("%d %B %Y %H:%M:%S")}\n' \
                             f'{website[0]} ' \
                             f'error {response.status_code}'
                    await message.answer(result)
                print(result)

            # Интерпретация кодов ошибок: https://www.restapitutorial.com/httpstatuscodes.html
            except:
                result = f'{datetime.now().strftime("%d %B %Y %H:%M:%S")}\n' \
                         f'{website[0]}' \
                         ' не отвечает'
                print(result)
                await message.answer(result)
#   send_message("Тестовое сообщение")
        time.sleep(600)

#Пишем handler для получения кроссовок
@dp.message_handler(Text(equals="Кроссовки"))
async def get_discount_sneakers(message: types.Message):
    await message.answer("Собираю данные, подождите секундочку...")
    collect_data()

    with open('result_data.json') as file:
        data = json.load(file)

    for item in data:#Идём по словарю и формируем карточки для вывода данных в бота
        card = f"{hlink(item.get('title'), item.get('link'))}\n" \
            f"{hbold('Категория: ')} {item.get('category')}\n" \
            f"{hbold('Прайс: ')} {item.get('price_base')}\n" \
            f"{hbold('Прайс со скидкой: ')} -{item.get('discount_percent')}%: {item.get('price_sale')}🔥"

        await message.answer(card)

@dp.message_handler(Text(equals="Мониторинг сайтов"))
async def get_sites_monitoring(message: types.Message):
    await message.answer('Секундочку, проверяю сайты...')

    for index, website in df_sites.iterrows():
        try:
            response = requests.get(
                website[0])  # Делаем запрос к нужному сайту и сохраняем данные в переменную response
            # print(website[0], " is ", response.status_code)
            if response.status_code == 200: #Форматирование https://docs-python.ru/standart-library/modul-datetime-python/kody-formatirovanija-strftime-strptime-modulja-datetime/
                result = f'{datetime.now().strftime("%d %B %Y %H:%M:%S")}\n' \
                         f'{website[0]} ' \
                         'OK'
            else:
                result = f'{datetime.now().strftime("%d %B %Y %H:%M:%S")}\n' \
                         f'{website[0]} ' \
                         f'error {response.status_code}'
            print(result)
            await message.answer(result)
        # Интерпретация кодов ошибок: https://www.restapitutorial.com/httpstatuscodes.html
        except:
            result = f'{datetime.now().strftime("%d %B %Y %H:%M:%S")}\n'\
                f'{website[0]}'\
                ' не отвечает'
            print(result)
            await message.answer(result)

@dp.message_handler(Text(equals="Крупа"))
async def get_discount_sneakers(message: types.Message):
    await message.answer('Please wait Крупа')

# def send_message(message):
#
#     """
#     Посылаем сообщение пользователю
#     """
#     bot.send_message('@UserName', 'message 1', parse_mode='HTML', disable_web_page_preview=True)
#     bot.send_message(userid, message, parse_mode='HTML', disable_web_page_preview=True)
#     print('I am in send_message(message)')

def ping_host(address):
    """
    Логика приложения. Хост по умолчанию в сети. Если он перестает откликаться,
    то ему присваивается статус не в сети и отправляется сообщение. Как только он
    появляется в сети, происходит обратный процесс и тоже посылается сообщение.
    """

    if ping_url(address):
        if not address.status:
            address.status = True
            send_message(address + " is up again")
    else:
        if (address.status):
            address.status = False
            send_message(address + " is down")
    print('I am in ping_host(address)')

def ping_url(url):
    """
    Пинг хоста. Response list - это ответ библиотеки ping. По умолчанию она
    посылает четыре пакета. Если все пакеты пропали, то хост считается неактивным.
    """

    i = 0;

    try:
        response_list = ping(url)

        for response in response_list:
            if (not response.success):
                i += 1

        if (i == 4):
            return False
        else:
            return True

    except Exception as e:
        send_message(str(e))

    print('I am in ping_url(url)')

def main():
    executor.start_polling(dp)#Запускаем бота
    send_message('message')
    print('line 160')
    """
        Все просто. Бесконечный цикл, который пингует сервисы один за другим.
        """
    while True:
        print('I am in 153 string ')
        for index, website in df_sites.iterrows():
            ping_host(website[0])
            print('I am in 156 string trying ping_host(website[0])')

        time.sleep(600)


if __name__ == "__main__":
    main()
