import requests
import lxml
from lxml import html
from lxml import etree

link = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?customerIdOrg=129560203%3A%D0%90%D0%94%D0%9C%D0%98%D0%9D%D0%98%D0%A1%D0%A2%D0%A0%D0%90%D0%A6%D0%98%D0%AF+%D0%9F%D0%9E%D0%A1%D0%95%D0%9B%D0%95%D0%9D%D0%98%D0%AF+%D0%A1%D0%9E%D0%A1%D0%95%D0%9D%D0%A1%D0%9A%D0%9E%D0%95zZ01483000083zZ651103zZ345865zZ5003057029zZ&af=on'
headers= {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36"}
r = requests.get(link, headers=headers)

# with open('output.html', 'a', encoding="utf-8") as f:
# 	f.write(r.text)

# class="search-registry-entrys-block"

root = lxml.html.fromstring(r.text)
title_elem = root.xpath('//title')[0].text

entry_cards = root.xpath('//*[contains(@class,"search-registry-entrys-block")]')


for e in entry_cards:
	print(e.text)
	# contract_num = e.find(class_,'registry-entry__header-mid__number').text
	# price = e.find(class_,"price-block__value").text

	# print(contract_num,price)