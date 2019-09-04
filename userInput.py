#This script needs to be run manually be the user
#It needs to be run in order to define the settings of the system
#These settings are saved in settings.log
#If the script is run once settings have already need set then the user has the 
#option to create new settings and delete the old or just view the settings
#some settings are not user defined and are set in this file.
#Once the setting have been set or changed an email is sent to the user to verify that the 
#system is operating correcctly

import os
from datetime import datetime
import json
from verifySystem import systemTest

#file path definitions
folderPath = "/home/pi/repos/freezerTemperatureMonitor/%s"
pathOfSettings = folderPath%"settings.log"
database = folderPath%'temperature_db'


#generic function for getting and proccessing user input
def get_input(message, default = False, defaultValue = 1):
#default and defaultValue have default values so function call doesnt need to include them
	text_input = input(message) #gets user input
	text_user = (text_input.rstrip()).lstrip() #strips any white space at the beginning or end of the input
	#if there is no default value and no input from the user, they are asked to input again
	if (default == False and len(text_user) == 0):
		print("Nothing Entered please try again")
		get_input(message)
	#if there is an default and no input from the user, the default value is returned
	elif (default == True and len(text_user) == 0):
		return defaultValue
	else:
	#If the user inputs then that is returned
		return text_user


def userSettings():
	#get user data
	#output: data in dictory object
	#clears the terminal
	print(chr(27) + "[2J")
	print("Hello, lets have a go at setting up the temperature monitor system, please answer the following questions..")
	location = get_input("Please enter the location of your freezer: ")

	freezerID = get_input("Please enter Freezer ID: ")

	tempLimit = get_input("Please enter your temperature limit in degrees celsius): ") 
	#asks for the recieve email twice to verify its correct. 
	while True:
		rxEmail = get_input("Please enter the email address that will recieve temperature alerts: ")
		rxEmail2 = get_input("Please confirm the email address that will recieve temperature alerts: ")
		if rxEmail == rxEmail2:
			break
		else:
			print("Emails do not match, please try again")

	#defaults settings that are not set by the user but are saved in the settings.log file
	holdEmail = 60
	checkTempInterval = 2
	txEmail = '' #hard code email here 
	pswd = '' #hard code password here
	#currently this system will not work as the email and password are not set. Created your own account or talk to the authour 

	#create a dictory of the settings
	dictSettings = {}
	dictSettings.update({'location':location})
	dictSettings['freezerID'] = freezerID
	dictSettings['checkTempInterval'] = checkTempInterval
	dictSettings['holdEmail'] = holdEmail
	dictSettings['tempLimit'] = tempLimit
	dictSettings['rxEmail'] = rxEmail
	dictSettings['txEmail'] = txEmail
	dictSettings['pswd'] = pswd
	dictSettings['timeInitialise'] = datetime.strftime(datetime.today(),'%y-%m-%d %H:%M:%S')
	return dictSettings	 

#pass in the settings path and extract the string Dictory
#turn that back into a dictory object and return it
def getSettings(settingsPath):
	with open(settingsPath,'r') as file:
		settings_str = file.read()
	if len(settings_str) == 0:
		print("Empty settings file....now deleted...please run program again")
		#if there is a file with nothing in it then remove that file and quit the program
		os.remove(settingsPath)
		quit()
	settings = json.loads(settings_str)			
	return settings
		

#displays the settings on the stdout
def displaySettings(settingsPath):

	#get the settings saved in setting file into a dictory object
	settings = getSettings(settingsPath)
	#extract the individual settings using the keys
	location = settings['location']
	freezerID = settings['freezerID']
	tempLimit = settings['tempLimit']
	rxEmail = settings['rxEmail']
	checkInterval = settings['checkTempInterval']
	holdEmail = settings['holdEmail']
	tempLimit = settings['tempLimit']
	txEmail = settings['txEmail']

	print(chr(27) + "[2J") # clear terminal
	#Print out the setting information for the user
	print("Here are the user defined system settings")
	print("-----------------------------------------\n")
	print("Device location set to: %s" % location)
	print("Freezer ID set to: %s" % freezerID)
	print("Email alerts will be sent too: %s" % rxEmail)
	print("The temperature alert is set too: %s\n" % str(tempLimit))
	print("------------------------------------------\n")
	print("The following settings can be chnaged by the administrator")
	print("------------------------------------------\n")
	print("Email alerts are sent from: %s" % txEmail)
	print("The time period the measured temperature is over the")
	print("temperature limit before an alert is sent: %s minutes" % str(checkInterval))
	print("The temperaure duration after an email alert that the temperature is checked")
	print("again: %s minutes" % holdEmail)
	print("-------------------------------------------\n")

	
def choiceDeleteSettings(path):
	#ask the user if they want to delete their settings file
	delete = input("Do you want to delete the current settings and enter new ones (Y/N)?")
	if delete == 'Y' or delete == 'y':
		#delete file and go to create new settings
		os.remove(path)
		print("Settings file deleted please enter new settings")
		#go to settings file
		return True
	elif delete == 'N' or delete == 'n':
		#exit the program
		print("The settings will stay the same, exiting program.....Goodbye")
		quit()
	else:
		print("Incorrect response, please try again")
		choiceDeleteSettings(path)
	
#--------------------------------------------------------------------
#Main program							-----				
#--------------------------------------------------------------------
	
if os.path.exists(pathOfSettings):
	#file exists so settings have already been set
	displaySettings(pathOfSettings)
	choiceDeleteSettings(pathOfSettings)
	#in the choiceDeleteSettings function, if you dont delete the function quits the program
	#if you do delete then you want to get setting and write to setting.log as you would if 
	#there were no settings

#asks user to input settings and returns them as dictory object
dict_settings = userSettings()
#write settings to a new file, use 'w' to overwrite any pre-existing file
#json.dumps turns the dictory object into a json string
with open(pathOfSettings,'w') as file:
	file.write(json.dumps(dict_settings))
displaySettings(pathOfSettings)
print("Thank you for completing the settings, an email will be sent to your specified email address to confirm the Freezer Monitor operations, goodbye")
#send verification email
systemTest(pathOfSettings,database)
print("Sent email")
	
	
    



		
