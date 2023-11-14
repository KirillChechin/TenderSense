import sqlite3
import time, datetime
import urllib.parse

records_per_page = 500

base = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?'
# region = 'delKladrIds=5277327%2C5277335&delKladrIdsCodes=50000000000%2C77000000000&'
region='customerPlace=5277327%2C5277335&customerPlaceCodes=50000000000%2C77000000000&'
params = f'sortBy=UPDATE_DATE&recordsPerPage=_{records_per_page}&fz44=on&fz223=on&af=on&'
start_price ='priceFromGeneral=1000000&'

past_date = datetime.datetime.today()-datetime.timedelta(days=5)
format_date = past_date.strftime("%d.%m.%Y")
param_date = f"publishDateFrom={format_date}&"

def vip_orgs():
	connection = sqlite3.connect('tender_info.db')
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
	connection = sqlite3.connect('tender_info.db')
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
		result = base+params+start_price+param_date+region+okpd_param

	return result+"&"

def log_tender(gk_num,price=0):
	connection = sqlite3.connect('tender_info.db')
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
	connection = sqlite3.connect('tender_info.db')
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
	connection = sqlite3.connect('tender_info.db')
	cursor = connection.cursor()
	cursor.execute('SELECT is_stale FROM tenders WHERE gk_num = ?',(gk_num,))
	tender = cursor.fetchall()[0][0]
	connection.close()
	return bool(tender)

def vip_count():
	connection = sqlite3.connect('tender_info.db')
	cursor = connection.cursor()
	cursor.execute('SELECT COUNT(DISTINCT inn) FROM orgs')
	count = cursor.fetchall()[0][0]
	return count

def okpd_count():
	connection = sqlite3.connect('tender_info.db')
	cursor = connection.cursor()
	cursor.execute('SELECT COUNT(DISTINCT id) FROM okpd')
	count = cursor.fetchall()[0][0]
	return count

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
	# print(search_query)
	print(all_okpd(),"\n")
	print(len(all_okpd()))
	# print(all_okpd(param_only=True))
	# print(okpd_count())
	print(url_param())



