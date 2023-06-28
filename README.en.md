# Parser telegram bot
## Изменить язык: [Русский](README.md)
***
Forwards messages from one channel to another, changing them to the desired format, has a message search function.

## Commands (sent to a separate chat with the bot):
- add - adds data (eg /add Tinkoff Tinkoff)
- name - adds a number, name (eg /add +79834628281 Vitya)
- all_names - displays all numbers and names saved in the database
- all_sources - displays all data of type (Tinkoff Tinkoff) stored in the database
- delete_name - deletes an entry from the database by phone number (eg /delete_name +79834628281)
- delete_source - deletes an entry from the database by the first name (eg /delete_source Tinkoff)
- search - searches through messages (eg /search query)

## Installation and use:
- error logging occurs in the py_log.log file
- create and activate virtual environment (if necessary):
```sh
python3 -m venv venv
source venv/bin/activate # for mac
source venv/Scripts/activate # for windows
```
- install dependencies:
```sh
pip install -r requirements.txt
```
- **You need to grant access to channel/group messages** (go to [BotFather](https://t.me/BotFather), select the appropriate bot -> Bot settings -> Group Privacy -> Turn off)
- **Bot must have permission to join groups** (go to [BotFather](https://t.me/BotFather), select the appropriate bot -> Bot settings -> Allow groups -> Turn groups on)
- **Bot must be added as an administrator of channels/groups** (change in the upper right corner of the profile channel -> administrators -> add administrator, allow sending messages)
- in file .env:\
Telegram bot token: **TELEBOT_TOKEN**=TOKEN\
Time in seconds during which identical messages are considered duplicates: **SECONDS=**60\
Channel ID from which the message is taken: **SOURCE_ID**=ID\
Channel ID where the message is sent: **TARGET_ID**=ID
> To determine the channel ID, forward any channel post to the next [bot](https://t.me/getmyid_bot). The value contained in **Forwarded from chat** is the channel ID\

**If the source where the message is retrieved from or where it is redirected to is not a channel, but is a chat (group), then its ID can be viewed in the console after sending any message to this chat, after including the bot there, granting it rights administrator and setting up access to messages**
- run the project:
```sh
python3 main.py
```