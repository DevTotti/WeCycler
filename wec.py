#import important libraries
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.select import Select as Sel

import re
import time
from bs4 import BeautifulSoup as bsp
import requests


cycler = []
entry = []
final_date = []
selectors = []

def chrome_drive():
	driver = webdriver.Chrome(executable_path = '/home/gitvee/workspace/extensions/chromedriver_linux64/chromedriver')

	driver.wait = WebDriverWait(driver, 5)

	return driver

def login(driver):
	driver.get("http://wecyclers-admin.cloudapp.net/login/?next=/")

	username = "Wecyclers"
	#password = input("Insert your password: ")
	#pswd = str(password)
	pswd = "1nigeria6"

	driver.find_element_by_id("id_username").send_keys(username)
	driver.find_element_by_id("id_password").send_keys(pswd)
	driver.find_element_by_id("id_password").send_keys("\n")

	getAdmin_data(driver)

def getAdmin_data(driver):
	driver.get("http://wecyclers-admin.cloudapp.net/admin/back_ends/reconcile_pickup/")
	#address = []

	cycler = driver.find_elements_by_class_name("field-__str__")
	for i in cycler:
		data = (str(i.text))
		cycler = list(data.split(' - '))
		cycler_id = cycler[1]
		log_id = cycler[0]
		output = "cycler id: "+cycler_id
		#address.append(log_id)
		#print (log_id, output)
		cycler.append(cycler_id)
		entry.append(log_id)



	for i in range(1,3):
		selector = "#result_list > tbody > tr:nth-child("+str(i)+") > th > a"

		selectors.append(selector)

	for url in selectors:
		links = driver.find_element_by_css_selector(str(url))
		#time.sleep(5)
		links.click()


		date = driver.find_element_by_css_selector('input.vDateField')

		real_date = date.get_attribute('value')
		#print (real_date)
		final_date.append(real_date)


		#getRecon_data(driver, cycler_id, real_date)


		driver.back()


def getRecon_data(driver,final_date):
	driver.get("http://wecyclers-admin.cloudapp.net/v2/#/pickup-reconciliation")

	#for cycler_id in cycler:
		#cycler_id = str(cycler_id)
		#obj = Select(driver.find_element_by_css_selector("option[value='{}']").format(cycler_id))

	for date in final_date:
		print (date)
		en_date = driver.find_elements_by_css_selector("input[type='text']")
		#start_date = en_date.get_attribute('class')
		for i in en_date:
			i.send_keys(Keys.CONTROL + "a")
			i.send_keys(date)

			driver.find_element_by_css_selector('.btn.btn-primary').send_keys('\n')


		columns = driver.find_elements_by_tag_name('th').text
		rows = driver.find_elements_by_tag_name('td').text
		for items in range(len(columns)):
			print (rows[items])


driver = chrome_drive()
login(driver)
getRecon_data(driver,final_date)




"""			try:
				en_date = driver.find_elements_by_css_selector("input.form-control")
		#start_date = en_date.get_attribute('class')
				for i in en_date:
					i.send_keys(Keys.CONTROL + "a")
					i.send_keys(date)

					driver.find_element_by_css_selector('.btn.btn-primary').send_keys('\n')
					print("Two working")
			except:
				print("Two failed")

				try:
					en_date = driver.find_elements_by_css_selector("input#type='text'")
		#start_date = en_date.get_attribute('class')
					for i in en_date:
						i.send_keys(Keys.CONTROL + "a")
						i.send_keys(date)

						driver.find_element_by_css_selector('.btn.btn-primary').send_keys('\n')
						print("Three working")
				except:
					print ("Error processing all elements")"""


		#columns_list = ['S/N','TimeStamp']
		#columns = driver.find_elements_by_xpath('//thead//tr//th')
		#for col in columns:
			#print (col.text)
		#	columns_list.append(str(col.text))











"""
			try:

				cycler_id = '11185'
				obj = Select(driver.find_elements_by_tag_name("select"))
				obj.select_by_value(cycler_id)
				print("three working1")
				pass

			except Exception as error:
				print (error, "three failed1")

				try:

					cycler_id = 'Berger Ibrahim Ibrahim - 11185'
					obj = Select(driver.find_elements_by_tag_name('select')).select_by_visible_text(cycler_id)
					print("four working1")
					pass

				except Exception as error:
					print(error, "Still not working1")"""













"""	cycler = driver.find_elements_by_class_name("field-__str__")
	for i in cycler:
		data = (str(i.text))
		cycler = list(data.split(' - '))
		cycler_id = cycler[1]
		log_id = cycler[0]
		output = "cycler id: "+cycler_id
		entry.append(log_id)"""













	#selector = driver.find_elements_by_xpath('//tbody//tr//th//a')
		#selectors.append(selector)