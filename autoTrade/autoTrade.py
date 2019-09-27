#encoding=utf8
#pip install PyUserInput
#https://blog.csdn.net/u012067766/article/details/79793264
from pymouse import PyMouse
from pykeyboard import PyKeyboard


from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import requests, json

import time

import os, sys

import numpy as np



def getCurDir():
	return os.path.dirname(os.path.realpath(__file__))

def getToday():
	today = time.localtime(time.time())
	today = today.strftime("%Y%m%d")
	return today


def buy(code):
	myMouse = PyMouse()
	myKeyboard = PyKeyboard()

	driver = webdriver.Chrome(os.path.join(getCurDir(), "chromedriver"))

	driver.maximize_window()
	driver.get("https://passport2.eastmoney.com/pub/login?backurl=http%3A//www.eastmoney.com/")
	#driver.get("https://hippo.gf.com.cn/?source=STORE & needLoginTrade=true#StockTrade")
	wait = WebDriverWait(driver, 30, .5)
	frame_login = wait.until(EC.presence_of_element_located((By.ID, "frame_login")))

	driver.switch_to.frame(frame_login)
	 
	wait.until(EC.presence_of_element_located((By.ID, "txt_account")))
	wait.until(EC.presence_of_element_located((By.ID, "txt_pwd")))

	driver.execute_script("document.getElementById('txt_account').value='15521262430';")
	driver.execute_script("document.getElementById('txt_pwd').value='Kobe780823';")


	time.sleep(5)
	myMouse.click(966, 500, 1)
	time.sleep(2)
	myMouse.click(966, 500, 1)
	driver.find_element_by_id("btn_login").click()

	divCaptcha = wait.until(EC.presence_of_element_located((By.ID, "divCaptcha")))
	mouse_action = ActionChains(driver)
	mouse_action.move_to_element_with_offset(divCaptcha, 15, 40).click().perform()
	mouse_action.click().perform()

	wait.until(EC.presence_of_element_located((By.ID, "unamepop"))).click()

	driver.switch_to.window(driver.window_handles[-1])
	wait.until(EC.presence_of_element_located((By.ID, "id_zuhe"))).click()

	driver.switch_to.window(driver.window_handles[-1])
	wait.until(lambda driver: driver.find_element_by_xpath("//span[contains(@class, 'm-trade')]")).click()

	driver.switch_to.window(driver.window_handles[-1])
	futcode = wait.until(EC.presence_of_element_located((By.ID, "futcode")))
	price = wait.until(EC.presence_of_element_located((By.ID, "price")))
	codenumber = wait.until(EC.presence_of_element_located((By.ID, "codenumber")))
	time.sleep(2)
	driver.execute_script("arguments[0].focus();", futcode)
	#windows
	#futcode.send_keys(Keys.CONTROL + "a")
	#MAC
	# myMouse.click(650,540,1)
	# myKeyboard.type_string('free87878660!')
	# myKeyboard.press_key('return')

	myMouse.click(400, 500, 1)
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')

	# futcode.send_keys(Keys.COMMAND + "a")
	# futcode.send_keys(Keys.DELETE)
	# futcode.send_keys(Keys.DELETE)
	# futcode.send_keys(Keys.DELETE)
	# futcode.send_keys(Keys.DELETE)
	time.sleep(1)
	# driver.execute_script("arguments[0].value='600519';", futcode)
	#futcode.send_keys("159928")
	futcode.send_keys(code)
	time.sleep(1)
	futcode.send_keys(Keys.ARROW_DOWN)
	# futcode.send_keys(Keys.ENTER)
	wait.until(lambda driver: driver.find_element_by_xpath("//div[contains(@class, 'nobb')]")).click()

	# driver.execute_script("arguments[0].focus();", price)
	# price.send_keys(Keys.CONTROL + "a")
	# price.send_keys(Keys.DELETE)
	# driver.execute_script("arguments[0].value='2';", price)

	driver.execute_script("arguments[0].focus();", codenumber)
	codenumber.send_keys(Keys.CONTROL + "a")
	codenumber.send_keys(Keys.DELETE)
	driver.execute_script("arguments[0].value='100';", codenumber)

	time.sleep(1)

	wait.until(EC.presence_of_element_located((By.ID, "btnOrder"))).click()

	btn_dayK = wait.until(lambda driver: driver.find_element_by_xpath("//li[contains(text(), '日K')]"))
	driver.execute_script("arguments[0].click();", btn_dayK)

	btn_kdj = wait.until(lambda driver: driver.find_element_by_xpath("//li[contains(text(), 'KDJ')]"))
	driver.execute_script("arguments[0].click();", btn_kdj)

	time.sleep(1)
	#futcodeNum = "159928"
	#futcodeNum = "510500"
	beg = "20170101"
	end = getToday
	k_data_url = "http://42.push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.{0}&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=1&beg={1}&end={2}&ut=fa5fd1943c7b386f172d6893dbfba10b&cb=cb76085147199693".format(futcodeNum, beg, end)
	resp = requests.get(k_data_url)
	lens = len(resp.text)
	start = resp.text.find('(')
	# print(resp.text[start+1:lens-2])
	klines = json.loads(resp.text[start+1:lens-2]).get("data")["klines"]
	klines_dict = []
	for k in klines:
		items = k.split(',')
		date = items[0].strip('-')
		kaipan = items[1]
		shoupan = items[2]
		highest = items[3]
		lowest = items[4]
		k_dict = {}
		k_dict["date"] = date
		k_dict["kaipan"] = kaipan
		k_dict["shoupan"] = shoupan
		k_dict["highest"] = highest
		k_dict["lowest"] = lowest
		klines_dict.append(k_dict)


def sell(code):
	myMouse = PyMouse()
	myKeyboard = PyKeyboard()

	driver = webdriver.Chrome(os.path.join(getCurDir(), "chromedriver"))

	driver.maximize_window()
	driver.get("https://passport2.eastmoney.com/pub/login?backurl=http%3A//www.eastmoney.com/")
	# driver.get("https://hippo.gf.com.cn/?source=STORE & needLoginTrade=true#StockTrade")
	wait = WebDriverWait(driver, 30, .5)
	frame_login = wait.until(EC.presence_of_element_located((By.ID, "frame_login")))

	driver.switch_to.frame(frame_login)

	wait.until(EC.presence_of_element_located((By.ID, "txt_account")))
	wait.until(EC.presence_of_element_located((By.ID, "txt_pwd")))

	driver.execute_script("document.getElementById('txt_account').value='15521262430';")
	driver.execute_script("document.getElementById('txt_pwd').value='Kobe780823';")

	time.sleep(5)
	myMouse.click(966, 500, 1)
	time.sleep(2)
	myMouse.click(966, 500, 1)
	driver.find_element_by_id("btn_login").click()

	divCaptcha = wait.until(EC.presence_of_element_located((By.ID, "divCaptcha")))
	mouse_action = ActionChains(driver)
	mouse_action.move_to_element_with_offset(divCaptcha, 15, 40).click().perform()
	mouse_action.click().perform()

	wait.until(EC.presence_of_element_located((By.ID, "unamepop"))).click()

	driver.switch_to.window(driver.window_handles[-1])
	wait.until(EC.presence_of_element_located((By.ID, "id_zuhe"))).click()

	driver.switch_to.window(driver.window_handles[-1])
	wait.until(lambda driver: driver.find_element_by_xpath("//span[contains(@class, 'm-trade')]")).click()



	driver.switch_to.window(driver.window_handles[-1])
	futcode = wait.until(EC.presence_of_element_located((By.ID, "futcode")))
	price = wait.until(EC.presence_of_element_located((By.ID, "price")))
	codenumber = wait.until(EC.presence_of_element_located((By.ID, "codenumber")))
	time.sleep(2)
	driver.execute_script("arguments[0].focus();", futcode)
	# windows
	# futcode.send_keys(Keys.CONTROL + "a")
	# MAC
	# myMouse.click(650,540,1)
	# myKeyboard.type_string('free87878660!')
	# myKeyboard.press_key('return')

	# 定位卖出
	wait.until(lambda driver: driver.find_element_by_xpath("//span[contains(@class, 'tab_sale')]")).click()
	time.sleep(1)
	myMouse.click(400, 500, 1)
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')
	myKeyboard.press_key('delete')

	# futcode.send_keys(Keys.COMMAND + "a")
	# futcode.send_keys(Keys.DELETE)
	# futcode.send_keys(Keys.DELETE)
	# futcode.send_keys(Keys.DELETE)
	# futcode.send_keys(Keys.DELETE)
	time.sleep(1)
	# driver.execute_script("arguments[0].value='600519';", futcode)
	# futcode.send_keys("159928")
	futcode.send_keys(code)
	time.sleep(1)
	futcode.send_keys(Keys.ARROW_DOWN)
	# futcode.send_keys(Keys.ENTER)
	wait.until(lambda driver: driver.find_element_by_xpath("//div[contains(@class, 'nobb')]")).click()

	# driver.execute_script("arguments[0].focus();", price)
	# price.send_keys(Keys.CONTROL + "a")
	# price.send_keys(Keys.DELETE)
	# driver.execute_script("arguments[0].value='2';", price)

	driver.execute_script("arguments[0].focus();", codenumber)
	codenumber.send_keys(Keys.CONTROL + "a")
	codenumber.send_keys(Keys.DELETE)
	driver.execute_script("arguments[0].value='100';", codenumber)

	time.sleep(1)

	#wait.until(lambda driver: driver.find_element_by_xpath("//span[contains(@class, 'tab_sale')]")).click()
	wait.until(EC.presence_of_element_located((By.ID, "btnOrder"))).click()

	btn_dayK = wait.until(lambda driver: driver.find_element_by_xpath("//li[contains(text(), '日K')]"))
	driver.execute_script("arguments[0].click();", btn_dayK)

	btn_kdj = wait.until(lambda driver: driver.find_element_by_xpath("//li[contains(text(), 'KDJ')]"))
	driver.execute_script("arguments[0].click();", btn_kdj)

	time.sleep(1)
	# futcodeNum = "159928"
	# futcodeNum = "510500"
	beg = "20170101"
	end = getToday
	k_data_url = "http://42.push2his.eastmoney.com/api/qt/stock/kline/get?secid=0.{0}&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57&klt=101&fqt=1&beg={1}&end={2}&ut=fa5fd1943c7b386f172d6893dbfba10b&cb=cb76085147199693".format(
		futcodeNum, beg, end)
	resp = requests.get(k_data_url)
	lens = len(resp.text)
	start = resp.text.find('(')
	# print(resp.text[start+1:lens-2])
	klines = json.loads(resp.text[start + 1:lens - 2]).get("data")["klines"]
	klines_dict = []
	for k in klines:
		items = k.split(',')
		date = items[0].strip('-')
		kaipan = items[1]
		shoupan = items[2]
		highest = items[3]
		lowest = items[4]
		k_dict = {}
		k_dict["date"] = date
		k_dict["kaipan"] = kaipan
		k_dict["shoupan"] = shoupan
		k_dict["highest"] = highest
		k_dict["lowest"] = lowest
		klines_dict.append(k_dict)

	print()
#
# if __name__ == '__main__':
# 	main()


# http://42.push2his.eastmoney.com/api/qt/stock/kline/get?
# 	 secid=0.159928
# 	&fields1=f1,f2,f3,f4,f5
# 	&fields2=f51,f52,f53,f54,f55,f56,f57
# 	&klt=101
# 	&fqt=1
# 	&beg=20170101
# 	&end=20200101
# 	&ut=fa5fd1943c7b386f172d6893dbfba10b
# 	&cb=cb76085147199693