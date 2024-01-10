# TenderSense

## Установка
Требуется Python 3.10 или новее и следующие модули:
- telebot
- requests
- BeautifulSoup4
- openpyxl

## Доступ к телеграмм боту
Токен телеграм бота необходимо поместить в переменную "token" в файл с названием "bot_config.py" в одну папку с файлом bot.py
```python
token = '0000000000:xxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxx'
```
[Инструкция как сделать новый телеграм бот и получить токен.](https://core.telegram.org/bots/features#botfather)

## Запуск бота
"python3 bot.py" находясь в папке расположения бота.

# Готово
Далее описание кода для будующих меинтейнеров

### bot.py
Основнай файл. Принимает, читает, отвечает на сообщения пользователя.
### bot_config.py
Хранит токен телеграм бота.
### links.py
Генирирует ссылки с релевантыми параментрами.
Управляет базой данных с "теплыми" заказчиками и интересующими ОКПД.
Логирует запросы
### parse_logic.py
Используя ссылки сгененрированные links.py делает запрос, парсит ответ, создает отчет в формате xlsx.
### tender_info.db
Содержит таблицы orgs, okpd, tenders. orgs и okpd содержат информацию для генерации ссылок, tenders логирует встречающиеся тендеры.

## База данных бота tender_info.db
Предполагается наличие базы данных с названием tender_info.db в корневой папке бота.
Внутренняя структура базы cостоит из следующих таблиц:
### okpd
```SQL
CREATE TABLE tenders (
    gk_num    INTEGER PRIMARY KEY
                      UNIQUE
                      NOT NULL,
    timestamp INTEGER NOT NULL,
    is_stale  BOOLEAN DEFAULT (FALSE),
    price     INTEGER DEFAULT (0) 
);
```

### orgs
```SQL
CREATE TABLE orgs (
    inn  INTEGER PRIMARY KEY
                 UNIQUE
                 NOT NULL,
    link TEXT    NOT NULL,
    name TEXT
);
```

### tenders
```SQL
CREATE TABLE tenders (
    gk_num    INTEGER PRIMARY KEY
                      UNIQUE
                      NOT NULL,
    timestamp INTEGER NOT NULL,
    is_stale  BOOLEAN DEFAULT (FALSE),
    price     INTEGER DEFAULT (0) 
);
```

## Об авторе
TenderSense разработано Кириллом Чечиным
k.che4in@yandex.ru
https://github.com/KirillChechin/TenderSense

