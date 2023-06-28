import telebot
import logging
import threading

import config
import functions

logging.basicConfig(level=logging.ERROR, 
                    filename="py_log.log", 
                    filemode="w", 
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    )

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(chat_id=message.chat.id,
                     text=config.START_TEXT,
                     parse_mode='Markdown',
                     )

@bot.message_handler(commands=['add'])
def add_command(message):

    message_data = message.text.split(' ')
    if len(message_data) == 3:
        source = message_data[1]
        name = message_data[2]
        functions.add_source(source, name)
        bot.send_message(chat_id=message.chat.id,
                    text=f'Добавлено в базу данных {source} - {name}.')
        
    else:
        bot.send_message(chat_id=message.chat.id,
                    text='Неверный формат данных. Пример: /add Tinkoff Тинек',
                    )

@bot.message_handler(commands=['name'])
def name_command(message):
    message_data = message.text.split(' ')

    if len(message_data) == 3:
        number = message_data[1]
        name = message_data[2]

        if functions.validate_number(number):
            functions.add_person(name, number)
            bot.send_message(chat_id=message.chat.id,
                        text=f'Добавлено в базу данных {number} - {name}.')
            
        else:
            bot.send_message(chat_id=message.chat.id,
                    text='Неверный формат номера телефона.')
    else:
        bot.send_message(chat_id=message.chat.id,
                    text='Неверный формат данных. Пример: /name +779006005040',
                    )
        
        
@bot.message_handler(commands=['delete_name'])
def delete_name_command(message):

    message_data = message.text.split(' ')
    if len(message_data) == 2:
        number = message_data[1]

        if functions.is_in_names(number):
            functions.delete_person(number)
            bot.send_message(chat_id=message.chat.id,
                    text=f'Номер {number} удален из базы данных.')
            
        else:
            bot.send_message(chat_id=message.chat.id,
                    text='Номер отсутствует в базе данных.')
    else:
        bot.send_message(chat_id=message.chat.id,
                    text='Неверный формат данных. Пример: /delete_name +79996665544',
                    )
        

@bot.message_handler(commands=['delete_source'])
def delete_source_command(message):

    message_data = message.text.split(' ')
    if len(message_data) == 2:
        source = message_data[1]

        if functions.is_in_sources(source):
            functions.delete_source(source)
            bot.send_message(chat_id=message.chat.id,
                    text=f'Ресурс {source} удален из базы данных.')
            
        else:
            bot.send_message(chat_id=message.chat.id,
                    text='Ресурс отсутствует в базе данных.')
    else:
        bot.send_message(chat_id=message.chat.id,
                    text='Неверный формат данных. Пример: /delete_source Tinkoff',
                    )
        

@bot.message_handler(commands=['all_names'])
def all_names_command(message):

    numbers_info = functions.all_numbers()
    if numbers_info:
        replies = functions.construct_all_message(numbers_info)
        for reply in replies:
            try:
                bot.send_message(chat_id=message.chat.id,
                    text=reply)
            except:
                pass
    else:
        bot.send_message(chat_id=message.chat.id,
                    text='Таблица с номерами пуста.')

        
@bot.message_handler(commands=['all_sources'])
def all_sources_command(message):

    sources_info = functions.all_sources()

    if sources_info:
        replies = functions.construct_all_message(sources_info)
        for reply in replies:
            try:
                bot.send_message(chat_id=message.chat.id,
                    text=reply)
            except:
                pass

    else:
        bot.send_message(chat_id=message.chat.id,
                    text='Таблица с ресурсами пуста.')


@bot.message_handler(commands=['search'])
def all_sources_command(message):

    keyword = message.text.replace('/search ', '')

    messages = functions.search_by_keyword(keyword)

    if messages:
        replies = functions.construct_with_keyword_message(messages, keyword)

        for reply in replies:
            try:
                bot.send_message(chat_id=config.TARGET_ID,
                    text=reply)
            except:
                pass

    else:
        bot.send_message(chat_id=message.chat.id,
                    text='Нет сообщений с заданным ключевым словом.')


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(chat_id=message.chat.id,
                     text=config.HELP_TEXT,
                     parse_mode='Markdown',
                     )


@bot.message_handler(content_types=['text', 'photo', 'video', 'document'])
@bot.channel_post_handler()
def channel_post(message):
    print(message.chat.id)
    if str(message.chat.id) == config.SOURCE_ID:
        text = False
        if message.text:
            text = message.text
        elif message.caption:
            text = message.caption

        if text:
            if functions.is_format(text):
                new_message = functions.if_new_message(text)

                if new_message:
                    threading.Thread(daemon=True, target=functions.add_to_archive, args=(text,)).start()

                    port = functions.extract_port(text)
                    sender = functions.extract_from(text)
                    number = functions.extract_num(text)
                    refill = functions.extract_refill(text)
                    amount = functions.extract_amount(text)

                    if port and sender and number and amount and refill:
                        person_name = functions.get_person_name(number).upper()
                        source_name = functions.get_source_name(sender).capitalize()

                        reply = functions.construct_reply(name=person_name,
                                                        port=port,
                                                        number=number,
                                                        source=source_name,
                                                        refill=refill,
                                                        amount=amount,
                                                        )

                        try:
                            bot.send_message(chat_id=config.TARGET_ID,
                                            text=reply,
                                            )
                        except:
                            pass


if __name__ == '__main__':
    # bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass