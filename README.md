# Parser telegram bot
## Change language: [English](README.en.md)
***
Пересылает сообщения из одного канала в другой, изменяя их под нужный формат, имеет функцию поиска по сообщениям.

## Команды (отправляются в отдельный чат с ботом):
- add - добавляет данные (н.р /add Tinkoff Тинек)
- name - добавляет номер, имя (н.р /add +79834628281 Витя)
- all_names - отображает все номера и имена, сохраненные в базу данных
- all_sources - отображает все данные типа (Tinkoff Тинек), сохраненные в базы данных
- delete_name - удаляет запись из базы данных по номеру телефона (н.р /delete_name +79834628281)
- delete_source - удаляет запись из базы данных по первому названию (н.р. /delete_source Tinkoff)
- search - осуществляет поиск по сообщениями (н.р. /search запрос)

## Установка и использование:
- логирование ошибок происходит в файл py_log.log
- создать и активировать виртуальное окружение (если необходимо):
```sh
python3 -m venv venv
source venv/bin/activate # for mac
source venv/Scripts/activate # for windows
```
- установить зависимости:
```sh
pip install -r requirements.txt
```
- **Необходимо предоставить доступ к сообщениям каналов/групп** (перейти в [BotFather](https://t.me/BotFather), выбрать соответствующего бота -> Bot settings -> Group Privacy -> Turn off)
- **У бота должно быть разрешение на вступление в группы** (перейти в [BotFather](https://t.me/BotFather), выбрать соответствующего бота -> Bot settings -> Allow groups -> Turn groups on)
- **Бот должен быть добавлен в качестве администратора каналов/групп** (изм. в правом верхнем углу профиля канал -> администраторы -> добавить администратора, разрешить отправку сообщений)
- в файле .env:\
Токен телеграм бота: **TELEBOT_TOKEN**=ТОКЕН\
Время в секундах, в течение которого одинаковые сообщения считаются дублями: **SECONDS=**60\
ID канала, из которого забирается сообщение: **SOURCE_ID**=ID\
ID канала, куда отправляется сообщение: **TARGET_ID**=ID
> Для определения ID канала нужно переслать любую публикацию канала в следующий [бот](https://t.me/getmyid_bot). Значение, содержащееся в **Forwarded from chat** - ID канала\

**Если источник, откуда извлекается сообщение или куда оно перенаправляется - не является каналом, а представляет из себя чат(группу), то его ID можно посмотреть в консоли, после отправки любого сообщения в данный чат, предварительно включив туда бота, предоставив ему права администратора и настроив доступ к сообщениям**
- запустить проект:
```sh
python3 main.py
```