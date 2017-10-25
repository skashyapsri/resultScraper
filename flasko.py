from bs4 import BeautifulSoup
import requests
import csv
import pprint
from flask import request
from flask import Flask
from flask import render_template
from flask import send_file
import sys
from selenium import webdriver
from time import sleep
import pandas as pd 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

list2=[]
list1=[]
       
app=Flask(__name__)

@app.route('/')
def my_form():
    return render_template("index.html")
@app.route('/say', methods=['POST','GET'])
def my_form_post():

	region=request.form['region']
	clg=request.form['clgcode']
	year=request.form['year']
	branch=request.form['branch'] 	
	lrange=request.form['lran']
	hrange=request.form['hran']
	filename = str(region+clg+year+branch+'.csv')
	try:
		file = open(filename,'w')   # Trying to create a new file or open one
		file.close()
	except:
		print "error" # quit Python
	
	j=["%03d" % i for i in range(int(hrange))]
	for i in j:
	    list1.append(region+clg+year+branch+str(i))
	for usn in list1:
		driver(usn,filename)

	return send_file(str(filename),
                     mimetype='text/csv',
                     attachment_filename=str(filename),
                     as_attachment=True)

	
def driver(usn,filename):
	chrome_options = Options()
	chrome_options.add_argument("--headless --disable-gpu ")
	driver = webdriver.Chrome('C:/Users/skash/Desktop/chromedriver.exe',chrome_options=chrome_options)
	driver.get('http://results.vtu.ac.in/cbcs_17/index.php')
	sleep(1)
	 
	username_box = driver.find_element_by_name('usn')
	username_box.send_keys(usn)
	sleep(1)
	 
	login_box = driver.find_element_by_xpath("//input[@value='SUBMIT']")
	login_box.click()

	try:
		alert = driver.switch_to_alert()
		alert.accept()
		driver.quit()
	
	except:
		soup=BeautifulSoup(driver.page_source,'html.parser')
		table_body=soup.find(class_='panel-body')
		    
		data1=[]        
		for data in table_body.find_all('td'):
		       data1.append(str(data.text))

		list2.append(data1)
		#filex = str(file)
		#a,b,c,d,e = filex.split("'")

		with open(str(filename),'w') as f:
				writer =csv.writer(f)
				writer.writerows(list2)

		driver.quit()
	

if __name__ == '__main__':
    app.run(debug=True)