#! /usr/bin/env python
#This is the main script of the temperature monitoring program
#add it to /etc/rc.local to automatically start when the device is powered on
#The script initialy loops until it can find and read in the settings.log file
#This means that if the user has not configured the system yet, the system will 
#not be able to check the temperature and send an alert
#once the settings have been read in the program will move to its main loop
#In the main loop the program will constantly read in the current temperature and 
#check it against the temperature limit (user defined in settings)
#If the current temperature remains over the temperature limit for a certain amount of time
#then an email alert is sent to the user. The program will then pause and not check the temperature
#again for an hour, to avoid the user receiving constant email when the device is over temperature

import os
import json
import time
#from createPlot import plotData
#from sendEmail import send_email
from readdB import getLatestTemps
from datetime import datetime
import Adafruit_DHT
from emailClass import Email

folderPath = "/home/pi/repos/freezerTemperatureMonitor/%s"
#definitions
path = folderPath%"settings.log"
logoPath = folderPath%"logo.jpg"
database = folderPath%'temperature_db'
NumOfSamples = 10 #with one per minute that is the last two minutes
htmlfile = folderPath%"emailAlertInline2.html"

#temperature sensor
sensor = Adafruit_DHT.DHT22
#GPIO 27
pin = 27

#This function gathers and processes all the data for sending the email alert and then passes it to the send_email function
#to create and send the email. send_email function is in a different file
def sendEmailAlert(location,htmlfile, txEmail, rxEmail, pswd, imagePath, tempLimit, holdEmail, temperature, tableList):
		subject = "%s Freezer Temperature Alert" % location
		#get the inserted values for the html file
		tl = str(tempLimit)
		ci = str(checkTempInterval)
		he = str(holdEmail)
		fi = str(freezerID)
		insertValues = [location,tl,temperature,he]
		insertValues.extend(tableList)
		print("INSERT VALUES")
		print(insertValues)
		#send_email(htmlfile, insertValues, txEmail, rxEmail, pswd, subject, plotPath)
		#Create an email instance
		alertEmail = Email(txEmail,rxEmail,pswd,subject)
		alertEmail.HTMLfileWithVariables(htmlfile,insertValues)
		alertEmail.htmlAddImage(imagePath,'image1')
		alertEmail.sendHTMLEmail()


#Open settings file
while True:
	#Check if settings exist
	if os.path.exists(path):
		print("File exists\n")
		#if the settings exist open for processing
		with open(path,'r') as file:
			settings = file.read()
			print("Reading Settings\n")
			#check to see if there is any settings in the settings.log file
			if len(settings) != 0:
				#turn the settings string back into a dictory object 
				settingsD = json.loads(settings)
				print(settingsD)
				#extract the individual settings from the dictory object
				location = settingsD['location']
				freezerID = settingsD['freezerID']
				txEmail = settingsD['txEmail']		
				rxEmail = settingsD['rxEmail']
				holdEmail = settingsD['holdEmail']
				tempLimit = settingsD['tempLimit']
				checkTempInterval = settingsD['checkTempInterval']	
				pswd = settingsD['pswd']
				#break from this loop to enter the main loop now the settings
				#have been read in
				break
	print("File Doesnt Exist")
	time.sleep(10)
	#wait 10 seconds before checking again




count = 0
print("main loop")
#main loop of the program
while True:
	#get the current temperature
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
	#if the current temperature is less than temperature limit
	#enter the 'checking loop'
	if temperature > int(tempLimit):
		print("OverTemperature")
		count = count + 1
		time.sleep(1)
	else:
		print("UnderTemperature")
		time.sleep(1)
		count = 0
	#in the 'checking loop' if the temperature is less than the temperature
	#for a certain again of time then send an email alert
	if count > (60 * int(checkTempInterval)):
	#if count > 5:	
		#Produce Plot
		print("over temperature long enough")
		#open the database and get data from the last four hours
		multiList = getLatestTemps(database, NumOfSamples)
		#returned value is a list of list, break out into individual lists
		times = multiList[0]
		temps = multiList[1]
		dates = multiList[2]
		
		temps.reverse()
		times.reverse()

		tableList = []
		for i in range(0,10):
			tableList.append(times[i])
			tableList.append(temps[i])

		print(tableList)
		temp = round(temperature,2)
		#Send Email
		print("send email")
		sendEmailAlert(location,htmlfile, txEmail, rxEmail, pswd, logoPath, tempLimit,  holdEmail, temp, tableList)
		#hold checking the of temperature for a fixed amount of time
		print("Hold for %s minutes"%holdEmail)
		time.sleep(60*int(holdEmail))
		count = 0
		#resume checking












 
