#This script contains a function that is used to read in x amount of the latest data from the 
#specified database
import sqlite3

def getLatestTemps(database, amount, daily = False):
	#connect to db
	db = sqlite3.connect(database)
	cursor = db.cursor()
	#create a tuple that will pass the amount of data to read from the database
	input = (amount,)

	#by default the read database function will look at the tempData table
	#but when a weekly report is needed it will read from the tempDaily
	#table
	if daily:
		cursor.execute('''SELECT * FROM tempDaily ORDER BY rowid DESC LIMIT ?''',(input))
	else:
		#This query will select data from the bottom (or latest written data) from the 
		#database
		cursor.execute('''SELECT * FROM tempData ORDER BY rowid DESC LIMIT ?''',(input))
	#get all data from the query
	results = cursor.fetchall()
	list_temps = []
	list_times = []
	list_dates = []
	#each index in the list results contains a list of date, time and temp
	#loop through each value in the results list and extract the corresponding 
	#data and add them to the correct list
	for value in results:
		list_dates.append(value[0])
		list_times.append(value[1])
		list_temps.append(value[2])
	#create a list of all the lists above and return
	listOflists = (list_times, list_temps, list_dates)
	return listOflists



