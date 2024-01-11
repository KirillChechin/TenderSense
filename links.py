import sqlite3
import os
import time, datetime
from time import gmtime, strftime
import urllib.parse

base = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?'
# Далее описываются фильтры тендеров

# Только заказчкики из москвы и московской области
region='customerPlace=5277327%2C5277335&customerPlaceCodes=50000000000%2C77000000000&'

# fz44=on&fz223 Закупки по ФЗ-44 и ФЗ-22. 
# af=on Этап закупки - ПОДАЧА ЗАЯВОК,
records_per_page = 500
params = f'sortBy=UPDATE_DATE&showLotsInfoHidden=false&recordsPerPage=_{records_per_page}&fz44=on&fz223=on&af=on&'

# Минимальная цена тендера (1 млн. руб.)
start_price ='priceFromGeneral=1000000&'

# Только тендеры начиная с предыдущего рабочего дня. Праздники не учитыватся.
def prev_work_day(days=1):
	past_date = datetime.datetime.today()-datetime.timedelta(days)
	while past_date.weekday()>4:
		# print(past_date.strftime("%d.%m.%Y"),"is a weekend")
		past_date = past_date-datetime.timedelta(1)
	format_date = past_date.strftime("%d.%m.%Y")
	return f"publishDateFrom={format_date}&"


db_name = "tender_info.db"
def init_database(db_name):
	"""создать базу данных если нет существующей"""
	if not os.path.isfile(db_name):
		print("Нет существующей базы данных, будет создана новая")
		conn = None
		try:
			conn = sqlite3.connect(db_name)
			print(sqlite3.version)
		except Exception as e:
			print(e)
		finally:
			if conn:
				cursor = conn.cursor()

				cursor.execute("""CREATE TABLE IF NOT EXISTS okpd (
						id INTEGER PRIMARY KEY
									 UNIQUE
									 NOT NULL,
						code TEXT	NOT NULL,
						info TEXT
					);""")
				cursor.execute("""CREATE TABLE IF NOT EXISTS orgs (
						inn  INTEGER PRIMARY KEY
									 UNIQUE
									 NOT NULL,
						link TEXT	NOT NULL,
						name TEXT
					);""")
				cursor.execute("""CREATE TABLE IF NOT EXISTS  tenders (
						gk_num	INTEGER PRIMARY KEY
										  UNIQUE
										  NOT NULL,
						timestamp INTEGER NOT NULL,
						is_stale  BOOLEAN DEFAULT (FALSE),
						price	 INTEGER DEFAULT (0) 
					);""")
				conn.commit()
				conn.close()
	else:
		print("Существующая база данных:",db_name)


def vip_orgs():
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	cursor.execute('SELECT * FROM orgs')
	orgs = cursor.fetchall()
	connection.close()
	result = []
	for org in orgs:
		all_okpd_str = all_okpd(param_only=True)
		full_link= base+params+all_okpd_str+org[1]
		result.append((org[0],full_link,org[2]))
	return result # (inn,link,name)

def all_okpd(param_only=False):
	okpd_param = "okpd2IdsWithNested=on&okpd2Ids="
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	cursor.execute('SELECT id FROM okpd')
	okpd = cursor.fetchall()
	connection.close()

	for i in okpd:
		i= str(i[0])
		okpd_param += i+"%2C"

	if param_only:
		# partial url params
		result = okpd_param
	else:
		#full url
		result = base+params+start_price+prev_work_day(1)+region+okpd_param

	return result+"&"

def log_tender(gk_num,price=0):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	cursor.execute('SELECT gk_num FROM tenders WHERE gk_num = ?',(gk_num,))
	tender = cursor.fetchall()
	if tender:
		# print("tender exists",tender)
		pass
	else:
		cursor.execute('INSERT INTO tenders (gk_num, timestamp, price ) VALUES (?, ?,?)', (gk_num, time.time(), price))
		print("tender logged",gk_num)
	connection.commit()
	connection.close()
	return

def log_tender_stale(gk_num,is_stale=True):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	cursor.execute('SELECT gk_num FROM tenders WHERE gk_num = ?',(gk_num,))
	tender = cursor.fetchall()
	if tender:
		cursor.execute('UPDATE tenders SET "is_stale" = ?, timestamp = ? where "gk_num"=?;',(is_stale,time.time(),gk_num))
		# print("tender updated",tender, "set is_stale", is_stale)
		connection.commit()
		connection.close()
		return True
	else:
		connection.close()
		return False

def tender_is_stale(gk_num):
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	cursor.execute('SELECT is_stale FROM tenders WHERE gk_num = ?',(gk_num,))
	tender = cursor.fetchall()[0][0]
	connection.close()
	return bool(tender)

def vip_count():
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	cursor.execute('SELECT COUNT(DISTINCT inn) FROM orgs')
	count = cursor.fetchall()[0][0]
	return count

def okpd_count():
	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	cursor.execute('SELECT COUNT(DISTINCT id) FROM okpd')
	count = cursor.fetchall()[0][0]
	return count

def extract_add_okpd(link:str):
	"""Добавить ОКПД из ссылки в базу данных"""
	Ids = link.split("okpd2Ids=")[-1]
	Ids = Ids.split("&")[0]
	Ids = Ids.split("%2C")

	codes = link.split("okpd2IdsCodes=")[-1]
	codes = codes.split("&")[0]
	codes = codes.split("%2C")

	info = "Добавлено через бота " + strftime("%d.%m.%Y ", gmtime())
	okpds = list(zip(Ids,codes, [info]*len(codes)))

	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	for i in okpds:
		cursor.execute('INSERT OR IGNORE INTO okpd(id,code,info) VALUES (?, ?,?)', (i[0],i[1],i[2],))
		connection.commit()
	connection.close()

	return codes

def extract_add_orgs(link:str):
	"""Добавить организации из ссылки в базу данных"""
	param_name = "customerIdOrg="
	param = link.split(param_name)[-1]
	param = param.split("&")[0]
	params = param.split("%7C%7C%7C")

	orgs = []
	for p in params:
		org_inn = p.split("zZ")[-2]

		url_param = param_name + p

		org_name = p.split("zZ")[0]
		org_name = urllib.parse.unquote(org_name)
		org_name = org_name.split(":")[-1]
		org_name = org_name.replace("+", " ").replace("&quot;", '"')

		orgs.append([org_inn,url_param,org_name])

	connection = sqlite3.connect(db_name)
	cursor = connection.cursor()
	for o in orgs:
		cursor.execute('INSERT OR IGNORE INTO orgs(inn,link,name) VALUES (?, ?,?)', (o[0],o[1],o[2],))
		connection.commit()
	connection.close()

	return [o[2] for o in orgs]


if __name__ == '__main__':
	tend = {'buyer': ' ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ БЮДЖЕТНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ "РОССИЙСКИЙ ИНСТИТУТ ТЕАТРАЛЬНОГО ИСКУССТВА - ГИТИС" ', 'buyer_link': 'https://zakupki.gov.ru//epz/organization/view223/info.html?agencyId=590812', 'gk': 32312884268, 'gk_link': 'https://zakupki.gov.ru//epz/order/notice/notice223/common-info.html?noticeInfoId=15914431', 'subj': 'Выполнение работ по развитию системы видеонаблюдения в Учебно-театральном комплексе Российского института театрального искусства – ГИТИС', 'price': 7885076, 'pub_date': '23.10.2023', 'end_date': '02.11.2023', 'doc_link': 'https://zakupki.gov.ru//epz/order/notice/notice223/documents.html?noticeInfoId=15914431'}
	# log_tender_stale(tend["gk"],is_stale=False)
	# log_tender(tend["gk"], tend['price'])
	# log_tender_stale(tend["gk"],is_stale=True)
	# print(tender_is_stale(tend["gk"]))
	# print(vip_orgs())
	# print(vip_count())


	# search_query = vip_orgs()
	# search_query = [base+params+x[1] for x in search_query]
	# print("\n\n".join(search_query))

	# print(all_okpd(),"\n")
	# print(len(all_okpd()))
	# print(all_okpd(param_only=True))
	# print(okpd_count())
	# print(prev_work_day(days=3))

	# # Parse and add to DB
	# existing_okpd = "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_500&showLotsInfoHidden=false&fz44=on&fz223=on&af=on&priceContractAdvantages44IdNameHidden=%7B%7D&priceContractAdvantages94IdNameHidden=%7B%7D&priceFromGeneral=100000&currencyIdGeneral=-1&publishDateFrom=09.01.2024&customerPlace=5277327%2C5277335&customerPlaceCodes=50000000000%2C77000000000&okpd2IdsWithNested=on&okpd2Ids=73123%2C73158%2C73729%2C8876230%2C8877775%2C8878292%2C8878456%2C8879383%2C8886886%2C8886887%2C8886888%2C8886889%2C8886891%2C8886913%2C8887459%2C8889387%2C8889389%2C8889396%2C8889410%2C8889631%2C8889749%2C8889753%2C8889756%2C8889832%2C8890590%2C8890645%2C8890817%2C8891044%2C8891045%2C8891134%2C8891135%2C8891289%2C9347448%2C9370131%2C9370135%2C9370175&okpd2IdsCodes=42.99.29.100%2C71.12.19.100%2C32.50.13.170%2C80.20.1%2C27.11.25%2C33.12.19%2C43.29.19%2C84.24.19%2C26.30.50.111%2C26.30.50.112%2C26.30.50.113%2C26.30.50.114%2C26.30.50.119%2C26.40.33.110%2C27.90.70.000%2C33.13.19.000%2C33.14.19.000%2C33.20.12.000%2C33.20.42.000%2C41.20.20.290%2C43.21.10.140%2C43.21.10.180%2C43.21.10.290%2C43.99.40.190%2C61.10.30.190%2C63.11.21.000%2C70.10.10.110%2C80.10.19.000%2C80.20.10.000%2C84.25.11.110%2C84.25.11.120%2C95.12.10.000%2C71.12.12.190%2C33.12.29.900%2C33.20.39.900%2C84.22.12.900&selectedSubjectsIdNameHidden=%7B%7D&okdpGroupIdsIdNameHidden=%7B%7D&koksIdsIdNameHidden=%7B%7D&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0&contractPriceCurrencyId=-1&budgetLevelIdNameHidden=%7B%7D&nonBudgetTypesIdNameHidden=%7B%7D&gws=%D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8"
	# new_okpd = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz44=on&fz223=on&af=on&priceContractAdvantages44IdNameHidden=%7B%7D&priceContractAdvantages94IdNameHidden=%7B%7D&currencyIdGeneral=-1&okpd2Ids=8879542&okpd2IdsCodes=01.11.11.110&selectedSubjectsIdNameHidden=%7B%7D&okdpGroupIdsIdNameHidden=%7B%7D&koksIdsIdNameHidden=%7B%7D&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0&contractPriceCurrencyId=-1&budgetLevelIdNameHidden=%7B%7D&nonBudgetTypesIdNameHidden=%7B%7D&gws=%D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8'
	# print(extract_add_okpd(existing_okpd))
	# print(extract_add_okpd(new_okpd))


	existing_org = """https://zakupki.gov.ru/epz/order/extendedsearch/results.html?sortBy=UPDATE_DATE&showLotsInfoHidden=false&recordsPerPage=_500&fz44=on&fz223=on&af=on&okpd2IdsWithNested=on&okpd2Ids=73123%2C73158%2C73729%2C8876230%2C8877775%2C8878292%2C8878456%2C8879383%2C8886886%2C8886887%2C8886888%2C8886889%2C8886891%2C8886913%2C8887459%2C8889387%2C8889389%2C8889396%2C8889410%2C8889631%2C8889749%2C8889753%2C8889756%2C8889832%2C8890590%2C8890645%2C8890817%2C8891044%2C8891045%2C8891134%2C8891135%2C8891289%2C9347448%2C9370131%2C9370135%2C9370175%2C&customerIdOrg=25922551%3AГОСУДАРСТВЕННОЕ+БЮДЖЕТНОЕ+УЧРЕЖДЕНИЕ+ЗДРАВООХРАНЕНИЯ+ГОРОДА+МОСКВЫ+%26quot%3BДЕТСКАЯ+ГОРОДСКАЯ+КЛИНИЧЕСКАЯ+БОЛЬНИЦА+ИМЕНИ+З.А.+БАШЛЯЕВОЙ+ДЕПАРТАМЕНТА+ЗДРАВООХРАНЕНИЯ+ГОРОДА+МОСКВЫ%26quot%3BzZ03732000058zZ634197zZ124042zZ7733024083zZ"""
	new_org = """https://zakupki.gov.ru/epz/order/extendedsearch/results.html?morphology=on&sortBy=UPDATE_DATE&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&priceContractAdvantages44IdNameHidden=%7B%7D&priceContractAdvantages94IdNameHidden=%7B%7D&currencyIdGeneral=-1&customerIdOrg=4%3A%D0%90%D0%9A%D0%A6%D0%98%D0%9E%D0%9D%D0%95%D0%A0%D0%9D%D0%9E%D0%95+%D0%9E%D0%91%D0%A9%D0%95%D0%A1%D0%A2%D0%92%D0%9E+%26quot%3B%D0%93%D0%90%D0%97%D0%9F%D0%A0%D0%9E%D0%9C+%D0%93%D0%90%D0%97%D0%9E%D0%A0%D0%90%D0%A1%D0%9F%D0%A0%D0%95%D0%94%D0%95%D0%9B%D0%95%D0%9D%D0%98%D0%95+%D0%9E%D0%A0%D0%95%D0%9D%D0%91%D0%A3%D0%A0%D0%93%26quot%3BzZ06530000001zZ891600zZ418zZ5610010369zZ%7C%7C%7C5%3A%D0%90%D0%9A%D0%A6%D0%98%D0%9E%D0%9D%D0%95%D0%A0%D0%9D%D0%9E%D0%95+%D0%9E%D0%91%D0%A9%D0%95%D0%A1%D0%A2%D0%92%D0%9E+%26quot%3B%D0%93%D0%90%D0%97%D0%9F%D0%A0%D0%9E%D0%9C+%D0%93%D0%90%D0%97%D0%9E%D0%A0%D0%90%D0%A1%D0%9F%D0%A0%D0%95%D0%94%D0%95%D0%9B%D0%95%D0%9D%D0%98%D0%95+%D0%98%D0%92%D0%90%D0%9D%D0%9E%D0%92%D0%9E%26quot%3BzZ06330000001zZ839384zZ422zZ3730006498zZ&selectedSubjectsIdNameHidden=%7B%7D&okdpGroupIdsIdNameHidden=%7B%7D&koksIdsIdNameHidden=%7B%7D&OrderPlacementSmallBusinessSubject=on&OrderPlacementRnpData=on&OrderPlacementExecutionRequirement=on&orderPlacement94_0=0&orderPlacement94_1=0&orderPlacement94_2=0&contractPriceCurrencyId=-1&budgetLevelIdNameHidden=%7B%7D&nonBudgetTypesIdNameHidden=%7B%7D&gws=%D0%92%D1%8B%D0%B1%D0%B5%D1%80%D0%B8%D1%82%D0%B5+%D1%82%D0%B8%D0%BF+%D0%B7%D0%B0%D0%BA%D1%83%D0%BF%D0%BA%D0%B8"""
	print(extract_add_orgs(existing_org))






