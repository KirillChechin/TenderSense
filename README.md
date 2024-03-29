# TenderSense
TenderSense - телеграм-бот, делает отчет о разыгрываемых тендерах по выбранным выдам деятельности или от интересующих заказчиков.

Критерии попадания тендера в выдачу:
1. Только заказчкики из москвы и московской области
2. Закупки по ФЗ-44 и ФЗ-223. 
3. Этап закупки - ПОДАЧА ЗАЯВОК
4. Минимальная цена тендера - 1 млн. руб.
5. Только тендеры начиная с предыдущего рабочего дня. Праздники не учитыватся.

## Установка
Требуется Python 3.10 или новее и следующие модули:
- telebot
- requests
- BeautifulSoup4
- openpyxl

Доступ к телеграмм боту:
Создать файл `bot_config.py` в корневой папке бота
В созданный файл в переменную `token` необходимо поместить токен телеграм-бота.
```python
token = "0000000000:xxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxx"
```
[Инструкция как сделать новый телеграм бот и получить токен.](https://core.telegram.org/bots/features#botfather)

Добавьте базу данных `tender_info.db` с информацией о заказчиках и ОКПД в корневую папку бота. Получить базу из существующего бота можно командой `/data`.

## Запуск бота
`python3 bot.py` находясь в папке расположения бота.
[Как запустить файл Python с помощью Командной строки Windows](https://ru.wikihow.com/%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D1%82%D0%B8%D1%82%D1%8C-%D1%84%D0%B0%D0%B9%D0%BB-Python-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-%D0%9A%D0%BE%D0%BC%D0%B0%D0%BD%D0%B4%D0%BD%D0%BE%D0%B9-%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B8-Windows)

## Готово
Далее описание кода для будующих меинтейнеров

### `bot.py`
Основнай файл. Принимает, читает, отвечает на сообщения пользователя.
### `bot_config.py`
Хранит токен телеграм бота.
### `links.py`
Создает ссылки с релевантыми параментрами.
Управляет базой данных с заказчиками и интересующими ОКПД.
Логирует запросы
### `parse_logic.py`
Используя ссылки сгененрированные `links.py` делает запрос, парсит ответ, создает отчет в формате `.xlsx`.
### `reports/`
Папка `reports/` создается автоматически в процессе работы. В ней сохраняются все отчеты генерируемые ботом. Автоматическое удаление файлов не предусмотрено, удаление по усмотрению администратора.
### `tender_info.db`
Содержит таблицы orgs, okpd, tenders. Таблицы orgs и okpd содержат информацию для составления ссылок, tenders логирует встречающиеся тендеры. 
_Внимание_ При отсутвии базы данных будет создана пустая, если не добавить заказчиков или ОКПД в отчет попадет первая 1000 тендеров, соответвующих общим критериям.

# Об авторе
TenderSense разработано Кириллом Чечиным
k.che4in@yandex.ru
Актуальная версия кода: 
https://github.com/KirillChechin/TenderSense

