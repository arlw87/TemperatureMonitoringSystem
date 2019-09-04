#The purpose of this module is to ensure that the temperature_db does not get too
#large. Although the device has enough space for 100 years of data the concern is 
#a large database will have a serious impact on the systems performance

#The module will determine how many rows the database has and if there are 
#too many will delete some
#current settings will mean that 1 day of data is deleted once 100 days
#of data has been recorded. After this one day of data is deleted 
#every day, so there is never more than 100 days of data in the database


import time
import sqlite3
Path = '/home/pi/repos/freezerTemperatureMonitor/%s'
databasePath = Path%'temperature_db'
maxRows = 144000 #100 days of data if one recorded every minute
deleteRows = 1440 #1 days whorth of data if a record saved every minute


while True:
	#code will loop forever
	#get the amount of records in the tempData table
	db = sqlite3.connect(databasePath)
	cursor = db.cursor()
	command = 'SELECT count(*) FROM tempData;'
	cursor.execute(command)
	results = cursor.fetchone()
	count = results[0]
	#count is a number not a string
	#if the number of counted rows is greater than the maximum Rows set
	print (count)
	if count > maxRows:
		#delete some rows
		input = (deleteRows,) #needs to be a tuple
		cursor.execute('''DELETE from tempData ORDER BY rowid LIMIT ?''',input)
		db.commit()
	else:
		#do nothing
		print("Number of rows is less than maximum allowed")
	db.close()
	#check every hour
	time.sleep(3600)
