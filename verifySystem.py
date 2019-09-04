#this function will check that the temperature Monitor system is functioning this includes the
#database, temperature sensor and the email systeme
#It  will send an email to report the results of this check
#This is function is called form the userInput.py script when the system is first set up
#or when the settings are changed

import Adafruit_DHT
import sqlite3
import json
from emailClass import Email

#define temperature sensor attributes
sensor = Adafruit_DHT.DHT22
pin = 27
#GPIO pin 27

def systemTest(path, database):
	try:
		#check the temperature sensor
		#if any of this fails program will goto the except
		print("Reading temperature.......")
		humidity, temp = Adafruit_DHT.read_retry(sensor, pin)
		print("temperature is: {}".format(round(temp,2)))
		tempWorks = True
		statement = "The temperature is currently {} degree celsius".format(round(temp,2))
	except:
		print("temperature reading failed")
		tempWorks = False
		statement = "No temperature reading available"

	try:
		#does the database work if any of this code in the try block fails
		#it will move to the except
		print("Checking the database.......")
		#connect to database
		db = sqlite3.connect(database)
		print("connected")
		cursor = db.cursor()
		print("cursor")
		#send a read query
		cursor.execute('''SELECT * FROM tempData LIMIT 5''')
		db.commit()
		results = cursor.fetchall()
		#print(len(results))
		db.close()
		print("Database is good")
		dbWorks = True
	except:
		print("DB didnt work")
		dbWorks = False


	#set the strings to be inserted into the html file for the email
	if tempWorks == True:
		strtempWorks = "WORKING"
	else:
		strtempWorks = "NOT WORKING"
		
	if dbWorks == True:
		strdbWorks = "WORKING"
	else:
		strdbWorks = "NOT WORKING"

	#open settings file and get dictory object
	file_object = open(path,'r')
	contents = file_object.read()
	file_object.close()
	#turn settings string into a dictory object
	read_settings = json.loads(contents)
	#get the individual settings and process data for sending email
	location = read_settings['location']
	htmlfile = "verify.html"
	insertValues = [location, strtempWorks, strdbWorks, statement]
	sender_email = read_settings['txEmail']
	password = read_settings['pswd']
	receiver_email = read_settings['rxEmail']
	subject = "Verification of Freezer Temperature Monitor"
	imageLocal = "logo.jpg"
	print("Sending Email.....")
	#send email
	#create a new email instance
	verifyEmail = Email(sender_email,receiver_email,password,subject)
	verifyEmail.HTMLfileWithVariables(htmlfile,insertValues)
	#keyword image1 used in the html
	verifyEmail.htmlAddImage(imageLocal,'image1')
	verifyEmail.sendHTMLEmail()
	


	#send_email(htmlfile,insertValues, sender_email, receiver_email, password, subject,imageLocal)

	
