import sqlite3
import logging

database = sqlite3.connect("info.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
cursor = database.cursor()

try:
    # creates table with names and numbers
    cursor.execute('''CREATE TABLE numbers(
        id INTEGER PRIMARY KEY,
        name VARCHAR (30),
        number VARCHAR (15)
    )''')
except:
    logging.error('Numbers table already exists.')

try:
    # creates table with sources
    cursor.execute('''CREATE TABLE sources(
        id INTEGER PRIMARY KEY,
        source VARCHAR (30),
        name VARCHAR (15)
    )''')
except:
    logging.error('Sources table already exists.')

try:
    # creates archive table
    cursor.execute('''CREATE TABLE archive(
        origin TEXT,
        origin_lower TEXT,
        send TIMESTAMP
    )''')
except:
    logging.error('Archive table already exists.')


# cursor.execute(f"DELETE FROM sources WHERE id=2")
# database.commit()