import re
import sqlite3
import logging
import inspect
import datetime
import itertools

import config

def is_format(text: str) -> bool:
    text = text.lower()
    counter = 0

    if 'port:' in text:
        counter += 1
    if 'num:' in text:
        counter += 1
    if 'from:' in text:
        counter += 1
    if 'доступно' in text:
        counter += 1
    if '@' in text:
        counter += 1
    if 'счет rub.' in text:
        counter += 1
    
    if counter == 6:
        return True
    
    return False


def validate_number(number):
    regex = r'[^0-9+]'
    restricted_symbols = re.search(regex, number)

    if restricted_symbols:
        return False
    
    return True


def extract_port(text):
    regex = r'(?<=port:).+?(?=:)'
    port = re.search(regex, text.lower())

    if port:
        port = port.group().strip(' ').upper()

    return port


def extract_num(text):
    regex = r'(?<=num:).*[0-9+]+'
    num = re.search(regex, text.lower())

    if num:
        num = num.group().strip(' ')

    return num


def extract_from(text):
    regex = r'(?<=from:).+?(?=@)'
    sender = re.search(regex, text.lower())

    if sender:
        sender = sender.group().strip(' ').upper()

    return sender


def extract_amount(text):
    regex = r'(?<=доступно).*[\.,0-9+]+'
    amount = re.search(regex, text.lower())

    if amount:
        amount = amount.group().strip(' ').upper().replace(',', '.')

    return amount


def extract_refill(text):
    regex = r'(?<=счет rub\.)\s*[0-9.]+'
    refill = re.search(regex, text.lower())

    if refill:
        refill = refill.group().strip(' ').upper().replace(',', '.')

    return refill


def get_person_name(number):
    # creating database cursor
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    person_name = cursor.execute("SELECT name FROM numbers WHERE number=?", (number,)).fetchall()

    cursor.close()
    database.close()

    if person_name:
        person_name = person_name[0][0]
    else:
        person_name = 'НЕ ОПРЕДЕЛЕНО'

    return person_name


def get_source_name(source):
    # creating database cursor
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    source = source.upper()
    source_name = cursor.execute("SELECT name FROM sources WHERE source=?", (source,)).fetchall()

    cursor.close()
    database.close() 

    if source_name:
        source_name = source_name[0][0]
    else:
        source_name = source

    return source_name   


def construct_reply(name, port, number, source, refill, amount):
    reply = f'''
            \n{name} в {port}: {number}\
            \nFROM: {source}\
            \n+ {refill}\
            \nСчет: {amount} руб\
            '''
    return reply


def add_source(source, name):
    # creating database cursor
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    source = source.upper()
    name = name.upper()
    cursor.execute("INSERT INTO sources (source, name) VALUES (?, ?)", (source, name))

    logging.info(f'{inspect.currentframe().f_code.co_name}: В таблицу sources добавлены: {source}, {name}.')

    database.commit()
    cursor.close()
    database.close() 


def add_person(name, number):
    # creating database cursor
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    name = name.upper()
    cursor.execute("INSERT INTO numbers (name, number) VALUES (?, ?)", (name, number))

    logging.info(f'{inspect.currentframe().f_code.co_name}: В таблицу names добавлены: {number}, {name}.')

    database.commit()
    cursor.close()
    database.close() 


def delete_person(number):
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    cursor.execute("DELETE FROM numbers WHERE number=?", (number,))

    logging.info(f'{inspect.currentframe().f_code.co_name}: Из таблицы names удален {number}.')

    database.commit()
    cursor.close()
    database.close() 


def delete_source(source):
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    source = source.upper()
    cursor.execute("DELETE FROM sources WHERE source=?", (source,))

    logging.info(f'{inspect.currentframe().f_code.co_name}: Из таблицы sources удален {source}.')

    database.commit()
    cursor.close()
    database.close() 


def is_in_sources(source):
    # creating database cursor
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    source = source.upper()
    id = cursor.execute("SELECT id FROM sources WHERE source=?", (source,)).fetchall()

    cursor.close()
    database.close()

    if id:
        return True
    
    return False


def is_in_names(number):
    # creating database cursor
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    id = cursor.execute("SELECT id FROM numbers WHERE number=?", (number,)).fetchall()

    cursor.close()
    database.close()

    if id:
        return True
    
    return False


def all_sources():
    # creating database cursor
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    sources_info = cursor.execute("SELECT * FROM sources").fetchall()

    cursor.close()
    database.close()

    return sources_info


def all_numbers():
    # creating database cursor
    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    numbers_info = cursor.execute("SELECT * FROM numbers").fetchall()

    cursor.close()
    database.close()

    return numbers_info


def construct_all_message(info_all):
    replies = []
    count = 0
    reply_text = ''

    for num, info in enumerate(info_all):
        reply_text += f'{num + 1}. {info[1]} - {info[2]}.\n'
        count += 1

        if count == 50 or count == len(info_all):
            replies.append(reply_text)
            reply_text = ''
            count = 0
    
    return replies


def if_new_message(text):
    '''Checks if message already in archive.'''

    database = sqlite3.connect("info.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = database.cursor()

    time_filter = datetime.datetime.utcnow() - datetime.timedelta(seconds=config.SECONDS)

    message_info = cursor.execute(f"SELECT * FROM archive WHERE origin=? and send>'{time_filter}'", (text,)).fetchall()

    cursor.close()
    database.close() 

    if message_info:
        return False
    
    return True


def add_to_archive(text):
    '''Adds new message to archive.'''

    database = sqlite3.connect("info.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cursor = database.cursor()

    send_time = datetime.datetime.utcnow()
    origin_lower = text.lower().replace('\n', ' ')
        
    cursor.execute(f'''
            INSERT INTO archive (origin, origin_lower, send)
            VALUES (?, ?, ?)
            ''', (text, origin_lower, send_time,))

    database.commit()
    cursor.close()
    database.close() 


def search_by_keyword(keyword):
    '''Search messages by keyword.'''

    keyword = f'%{keyword.lower()}%'

    database = sqlite3.connect("info.db")
    cursor = database.cursor()

    messages = cursor.execute(f"SELECT origin FROM archive WHERE origin_lower LIKE ?", (keyword,)).fetchall()

    cursor.close()
    database.close() 

    if messages:
        messages = list(itertools.chain.from_iterable(messages))

    return messages


def construct_with_keyword_message(messages, keyword):

    replies = []

    count = 0
    reply_text = f'Сообщения, содержащие: {keyword}'

    for message in messages:
        port = extract_port(message)
        sender = extract_from(message)
        number = extract_num(message)
        refill = extract_refill(message)
        amount = extract_amount(message)

        if port and sender and number and amount and refill:
            person_name = get_person_name(number).upper()
            source_name = get_source_name(sender).capitalize()

            reply_text += construct_reply(name=person_name,
                                        port=port,
                                        number=number,
                                        source=source_name,
                                        refill=refill,
                                        amount=amount,
                                        )
            
            count += 1

            if count == 20 or count == len(messages):
                replies.append(reply_text)
                reply_text = f'Сообщения, содержащие: {keyword}'
                count = 0
    
    return replies


