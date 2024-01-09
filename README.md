# TenderSense

## Требуется Python 3.10+ и следующие модули:
- telebot
- requests
- BeautifulSoup4
- openpyxl

## Доступ к телеграмм боту
Токен телеграм бота необходимо поместить в переменную "token" в файл с названием "bot_config.py" в одну папку с файлом bot.py Пример:
```python
token = '0000000000:xxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxx'
```

## Запуск бота
"python3 bot.py" находясь в папке расположения бота

## Добавить или убрать отслеживаемые организации или ОКПД
### Добавляем ОКПД
1. На сайте закупок делаем поиск по интересующиему нас ОКПД.
2. Копируем ссылку из браузера и вычленяем из нее параметр отвечеющий за окпд.
Пример: в парметрах поиска выбираю ОКПД 42.99.29.100. Жду результатов поиска и копирую сслыку из браузера
```
https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&priceContractAdvantages44IdNameHidden=%7B%7D&priceContractAdvantages94IdNameHidden=%7B%7D&currencyIdGeneral=-1&okpd2Ids=73123&okpd2IdsCodes=42.99.29.100&selectedSubjectsIdNameHidden=%7B%7D&okdpGroupIdsIdNameHidden=%7B%7D&koksIdsIdNameHidden=%7B%7D&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0&contractPriceCurrencyId=-1&budgetLevelIdNameHidden=%7B%7D&nonBudgetTypesIdNameHidden=%7B%7D&gws=%D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8
```
Из всей сслыки интересует только параметры okpd2Ids и okpd2IdsCodes
```
okpd2Ids=73123&okpd2IdsCodes=42.99.29.100&
```
3. Добавляем в базу данных tender_info.db в таблицу okpd новую строку.
   id|code|info
   ---|---|---
   73123 |	42.99.29.100	| добавлено 01.01.2024

### Добавляем отслеживаюмую организацию
1. Ищем заказчика. Например по ИНН: 5000001525
2. Получаем резуьтаты поиска, копируем ссылку на страницу
   ```
   https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&priceContractAdvantages44IdNameHidden=%7B%7D&priceContractAdvantages94IdNameHidden=%7B%7D&currencyIdGeneral=-1&selectedSubjectsIdNameHidden=%7B%7D&okdpGroupIdsIdNameHidden=%7B%7D&koksIdsIdNameHidden=%7B%7D&participantName=5000001525&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0&contractPriceCurrencyId=-1&budgetLevelIdNameHidden=%7B%7D&nonBudgetTypesIdNameHidden=%7B%7D&gws=%D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8](https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&priceContractAdvantages44IdNameHidden=%7B%7D&priceContractAdvantages94IdNameHidden=%7B%7D&currencyIdGeneral=-1&customerIdOrg=19050534%3A%D0%93%D0%9E%D0%A1%D0%A3%D0%94%D0%90%D0%A0%D0%A1%D0%A2%D0%92%D0%95%D0%9D%D0%9D%D0%9E%D0%95+%D0%91%D0%AE%D0%94%D0%96%D0%95%D0%A2%D0%9D%D0%9E%D0%95+%D0%A3%D0%A7%D0%A0%D0%95%D0%96%D0%94%D0%95%D0%9D%D0%98%D0%95+%D0%9C%D0%9E%D0%A1%D0%9A%D0%9E%D0%92%D0%A1%D0%9A%D0%9E%D0%99+%D0%9E%D0%91%D0%9B%D0%90%D0%A1%D0%A2%D0%98+%26quot%3B%D0%9C%D0%9E%D0%A1%D0%90%D0%92%D0%A2%D0%9E%D0%94%D0%9E%D0%A0%26quot%3BzZ03482000497zZ794956zZ118714zZ5000001525zZ&selectedSubjectsIdNameHidden=%7B%7D&okdpGroupIdsIdNameHidden=%7B%7D&koksIdsIdNameHidden=%7B%7D&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0&contractPriceCurrencyId=-1&budgetLevelIdNameHidden=%7B%7D&nonBudgetTypesIdNameHidden=%7B%7D&gws=%D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8)https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&priceContractAdvantages44IdNameHidden=%7B%7D&priceContractAdvantages94IdNameHidden=%7B%7D&currencyIdGeneral=-1&customerIdOrg=19050534%3A%D0%93%D0%9E%D0%A1%D0%A3%D0%94%D0%90%D0%A0%D0%A1%D0%A2%D0%92%D0%95%D0%9D%D0%9D%D0%9E%D0%95+%D0%91%D0%AE%D0%94%D0%96%D0%95%D0%A2%D0%9D%D0%9E%D0%95+%D0%A3%D0%A7%D0%A0%D0%95%D0%96%D0%94%D0%95%D0%9D%D0%98%D0%95+%D0%9C%D0%9E%D0%A1%D0%9A%D0%9E%D0%92%D0%A1%D0%9A%D0%9E%D0%99+%D0%9E%D0%91%D0%9B%D0%90%D0%A1%D0%A2%D0%98+%26quot%3B%D0%9C%D0%9E%D0%A1%D0%90%D0%92%D0%A2%D0%9E%D0%94%D0%9E%D0%A0%26quot%3BzZ03482000497zZ794956zZ118714zZ5000001525zZ&selectedSubjectsIdNameHidden=%7B%7D&okdpGroupIdsIdNameHidden=%7B%7D&koksIdsIdNameHidden=%7B%7D&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0&contractPriceCurrencyId=-1&budgetLevelIdNameHidden=%7B%7D&nonBudgetTypesIdNameHidden=%7B%7D&gws=%D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8
   ```
   вычленяем параметр customerIdOrg. Важно: выделяем параметр от & до &. В получившемся выделении не должно быть &, только то что "между"

   ```
   customerIdOrg=19050534%3A%D0%93%D0%9E%D0%A1%D0%A3%D0%94%D0%90%D0%A0%D0%A1%D0%A2%D0%92%D0%95%D0%9D%D0%9D%D0%9E%D0%95+%D0%91%D0%AE%D0%94%D0%96%D0%95%D0%A2%D0%9D%D0%9E%D0%95+%D0%A3%D0%A7%D0%A0%D0%95%D0%96%D0%94%D0%95%D0%9D%D0%98%D0%95+%D0%9C%D0%9E%D0%A1%D0%9A%D0%9E%D0%92%D0%A1%D0%9A%D0%9E%D0%99+%D0%9E%D0%91%D0%9B%D0%90%D0%A1%D0%A2%D0%98+%26quot%3B%D0%9C%D0%9E%D0%A1%D0%90%D0%92%D0%A2%D0%9E%D0%94%D0%9E%D0%A0%26quot%3BzZ03482000497zZ794956zZ118714zZ5000001525zZ
   ```
3. Добавляем в базу данных tender_info.db в таблицу orgs новую строку.
   inn | link | name
   --- | :--- | ---
   5000001525 | customerIdOrg=19050534%3A%D0%93%D0%9E%D0%A1%D0%A3%D0%94%D0%90%D0%A0%D0%A1%D0%A2%D0%92%D0%95%D0%9D%D0%9D%D0%9E%D0%95+%D0%91%D0%AE%D0%94%D0%96%D0%95%D0%A2%D0%9D%D0%9E%D0%95+%D0%A3%D0%A7%D0%A0%D0%95%D0%96%D0%94%D0%95%D0%9D%D0%98%D0%95+%D0%9C%D0%9E%D0%A1%D0%9A%D0%9E%D0%92%D0%A1%D0%9A%D0%9E%D0%99+%D0%9E%D0%91%D0%9B%D0%90%D0%A1%D0%A2%D0%98+%26quot%3B%D0%9C%D0%9E%D0%A1%D0%90%D0%92%D0%A2%D0%9E%D0%94%D0%9E%D0%A0%26quot%3BzZ03482000497zZ794956zZ118714zZ5000001525zZ |	ГБУ МО «Мосавтодор»


## Структура кода
### bot.py
Основнай файл. Принимает, читает, отвечает на сообщения пользователя.
### bot_config.py
Хранит токен телеграм бота.
### links.py
Генирирует ссылки с релевантыми параментрами.
Управляет базой данных с "теплыми" заказчиками и интересующими ОКПД.
Логирует запросы
### tender_info.db
Содержит таблицы orgs, okpd, tenders. orgs и okpd содержат информацию для генерации ссылок, tenders логирует встречающиеся тендеры.
### parse_logic.py
Используя ссылки сгененрированные links.py делает запрос, парсит ответ, создает отчет в формате xlsx.
