#This script produces a daily or weekly report sent by email with the temperature profile of the freezer
#These are sent at a time or day dependent on the target time set in this file
from readdB import getLatestTemps
#from createPlot import plotData
from datetime import timedelta, datetime
import json
#from sendEmail import send_email
from emailClass import Email
import os
import time
from createPDF import CreatePDF

#definitions
folderPath = "/home/pi/repos/freezerTemperatureMonitor/%s"
type = "daily"
databasePath = folderPath%'temperature_db'
filename = folderPath%"logo.jpg"
htmlfile = folderPath%"weeklyEmail_Dynamic.html"
Settingspath = folderPath%"settings.log"

#the traget time is set to 13:15 for daily. The target day (for weekly) is set to Monday, as that is the day
#of the 18/02/2019
targetTime = datetime(2019,9,4,21,20,0,0)
#currentTime = datetime(2019,3,10,15,00,0,0)

#
while True:
	#get the current time and date
	currentTime = datetime.now()
	time.sleep(1)
	startSummary = False
	#if the current time is the time set to be the time of the day to send the email
	if targetTime.hour == currentTime.hour and targetTime.minute == currentTime.minute:
		print("Time Match")
		#This script will send out reports weekly
		if targetTime.weekday() == currentTime.weekday():
			print("weekly")
			#weekly report get data for every hour
			#NumOfSamples = 7
			#see above
			#This may take too long
			#amount of data in a week
			dbRows = 7
			#want one sample per hour for the graph
			#sample = 60
			startSummary = True
		else:
			startSummary = False
		
	#if a summary is required
	if startSummary:		
		#open the database and get data
		#optional third statement, used to select the tempDaily DB not tempData
		multiList = getLatestTemps(databasePath, dbRows, True)
		times = multiList[0]
		temps = multiList[1]
		dates = multiList[2]
	
		temps.reverse()
		dates.reverse()
		#lists need to be reverse due to the way they are read from the dB
	
		#create Date objects
		dateObjects = []
		
		for o in dates:
			dateObjects.append(datetime.strptime(o, "%Y-%m-%d"))
		
				
		#convert date object into a string date of Weekday - Day of Month - Month - Year
		strDates = []
		for d in dateObjects:
			strDates.append(datetime.strftime(d,"%a %d %B %Y"))
		
		#lists need to be reversed as first item is the latest data
		#due to the way its called from the dB
		print(strDates)
		print(temps)



		#to send an email i need to get the settings from the settings file to know where to sent it too
		#if the settings.log file doesnt exist then the email cant be sent
		if os.path.exists(Settingspath):
				print("File exists\n")
				#open settings file for reading
				with open(Settingspath,'r') as file:
					settings = file.read()
					print("Reading Settings\n")
					if len(settings) != 0:
						#turn the settings string back into a dictory object 
						settingsD = json.loads(settings)
						#extract the individual settings from the dictory
						location = settingsD['location']
						freezerID = settingsD['freezerID']
						txEmail = settingsD['txEmail']		
						rxEmail = settingsD['rxEmail']
						holdEmail = settingsD['holdEmail']
						tempLimit = settingsD['tempLimit']
						checkTempInterval = settingsD['checkTempInterval']	
						pswd = settingsD['pswd']
						sendEmail = True
					
		else:
				print("Not Settings Not Sending an email")
				sendEmail = False

		#generate insertValues
		insertValues = []
		insertValues.append(location)
		insertValues.append(strDates[0])

		for i in range(0,7):
			insertValues.append(strDates[i])
			insertValues.append(temps[i])		

		print(insertValues)
		print(len(insertValues))

		#generate PDF for attachment
		pdfName = "Freezer Report for {} week beginning {}.pdf".format(location,strDates[0])
		#save pdf into the reports folder
		pdfLocation = folderPath%"reports/"
		pdfLocation = pdfLocation + pdfName
		print(pdfLocation)
		attachPDF = CreatePDF(htmlfile,insertValues,pdfLocation)
		attachPDF.scaleA4PDF()

		#if the settings have been read in then the email can be created and sent
		if sendEmail:
			#sendEmail
			subject = "%s Freezer Weekly Temperature Readings" % location
			
			#create new email instance
			report = Email(txEmail,rxEmail,pswd,subject)
			report.defineAdvancedEmailPlain("Please See Attached for weekly temperature report")
			report.addAttachment(pdfName,pdfLocation)
			report.sendHTMLEmail()


		print("waiting....")
		time.sleep(120) #once it has the right hour and minute and sends email, dont want it to send another in that minute
		print("finished waiting")	



