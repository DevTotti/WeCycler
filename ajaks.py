#import important libraries
#---------> Code Author: DevTotti
#---------> Link/URL: www.github.com/DevTotti
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.select.Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.select import Select 
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException

import csv
import re
import time
from bs4 import BeautifulSoup as bsp
import requests
import pdb

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


all_cyclers = {"Gafar Magodo Franchise - 11113":"11113","kike manager - 11129":"11129","Wole Manager - 11131":"11131","Bowla Favour David - 11137":"11137","Wasiu Olasukanmi - 11146":"11146","Berger Ridwan Ridwan  - 11149":"11149","Lekan Franchise - 11150":"11150","Bowla Niyi Niyi - 11151":"11151","ayodele ademosu - 11152":"11152","Berger Manager Manager - 11153":"11153","Bowla Manager - 11154":"11154","Olusosun Manager - 11155":"11155","Agunlejika Manager - 11156":"11156","ire taiwo - 11157":"11157","Segun Franchise - 11158":"11158","Adeniran Azeez - 11160":"11160","Oriyomi Franchise - 11162":"11162","Franchise Makoko - 11163":"11163","Taiwo Sonibare - 11164":"11164","Sodiq berger berger - 11167":"11167","Berger Yemi Yemi - 11168":"11168","Berger Shola Shola  - 11170":"11170","Bowla Samuel Idumu - 11171":"11171","WREX SODIQ - 11172":"11172","Opeyemi  Oladejo - 11173":"11173","Sodiq Mufutau - 11174":"11174","Adeniran Azeez - 11175":"11175","Curbside Iyana Ipaja  - 11176":"11176","Berger Abdullah Abdullah - 11177":"11177","Magboro Franchise - 11179":"11179","Lekki Curbside Peace - 11180":"11180","Ejigbo Taiwo - 11181":"11181","Bowla Tayo Tayo - 11182":"11182","Ikorodu Curbside Abiodun  - 11183":"11183","Tolu Aderonmu - 11184":"11184","Berger Ibrahim Ibrahim - 11185":"11185","wisdom rider - 11186":"11186","Gbagada WERX WERX - 11187":"11187","Franchise Ikorodu Franchise - 11188":"11188"}


submit = []
cycler = []
entry = []
final_date = []
selectors = []

def chrome_drive():
	driver = webdriver.Chrome(executable_path = '/home/gitvee/workspace/extensions/chromedriver_linux64/chromedriver',chrome_options=chrome_options)

	driver.wait = WebDriverWait(driver, 5)

	return driver

def login(driver):
	driver.get("http://wecyclers-admin.cloudapp.net/login/?next=/")

	username = "put admin login name here"
	pswd = "put password here"

	driver.find_element_by_id("id_username").send_keys(username)
	driver.find_element_by_id("id_password").send_keys(pswd)
	driver.find_element_by_id("id_password").send_keys("\n")

	getAdmin_data(driver)

def getAdmin_data(driver):
	driver.get("http://wecyclers-admin.cloudapp.net/admin/back_ends/reconcile_pickup/")
	pages = driver.find_elements_by_xpath('//p//a')
	page = pages[-1].text
	page = int(page)
	#print (page)
	item = driver.find_element_by_xpath('//*[@id="changelist-form"]/div[1]/span[1]')
	items = item.text
	count = items.split()
	#print(count)
	items = int(count[-2])
	#print(items)
	items = int(items+1)
	item = 1


	for page_num in range(page):
		get = "http://wecyclers-admin.cloudapp.net/admin/back_ends/reconcile_pickup/?p="+str(page_num)
		driver.get(get)

		driver.implicitly_wait(3)
		selector = [link.get_attribute('href') for link in driver.find_elements_by_xpath("//tbody//tr//a")]
		#print(selector)
		pass



		for links in selector[item:items]:

			driver.get(links)

			date = driver.find_element_by_css_selector('input.vDateField')

			real_date = date.get_attribute('value')

			final_date.append(real_date)

			cyc = driver.find_element_by_id("id_wecycler")

			cycler_id = cyc.get_attribute('value')

			cycler.append(cycler_id)	


		driver.back()


		


def getRecon_data(driver,final_date, cycler):
	#driver.get("http://wecyclers-admin.cloudapp.net/v2/#/pickup-reconciliation")
	#print (cycler)
	#a = ['11151','11137']value
	#print(cycler)
	cycler_list = cycler
	date_list = final_date

	combination = dict(zip(date_list, cycler_list))
	print(combination)


	for dates, cycler in combination.items():

		try:
			driver.get("http://wecyclers-admin.cloudapp.net/v2/#/pickup-reconciliation")
			#dday = driver.find_element_by_css_selector('.btn.btn-primary')

			obj = Select(driver.find_element_by_css_selector('select.form-control'))
			obj.select_by_value(cycler)
			#print("Two Working1")
			pass

		except Exception as error:
			print(error, "Two failed")

		pass


##########################################################################################################################
		#a = ['2019-05-01']
		#driver.refresh()
		#print("Trying")

		en_date = driver.find_elements_by_xpath("//div//p//input")
		elements = []
			
		try:
			en_date[0].clear()
			en_date[1].clear()

			for i in en_date:

				i.send_keys(dates)


			driver.find_element_by_css_selector('.btn.btn-primary').send_keys('\n')

			data = [cycler,dates]
			time.sleep(2)
			elements = driver.find_elements_by_xpath('//tbody//tr//td')
			for entry in elements:
				new_data = entry.text
				new_data = new_data.split()
				final_data = new_data
				print(final_data)
				data.append(final_data)

			with open ('we_clean_data.csv','a') as newfile:
				print(data)
				writer = csv.writer(newfile)
				writer.writerow(data)

			driver.refresh()


		except Exception as error:
			print(error,"Error from here")



		driver.refresh()



driver = chrome_drive()
login(driver)
getRecon_data(driver,final_date,cycler)


