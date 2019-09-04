#write temperature data to database
#inputs temperature data, location, FreezerID, Time and Date, 
#does not return anything
from datetime import datetime, timedelta
import sqlite3
import time
import Adafruit_DHT

#definitions
Path = '/home/pi/repos/freezerTemperatureMonitor/{}'
dBPath = Path.format('temperature_db')
dataWriteFrequency = 60
#write data every 60seconds

#define temperature sensor 
sensor = Adafruit_DHT.DHT22
#GPIO PIN 27
pin = 27

#defined as a fucntion
def temperature_db(dBFile, table):
	#get the temperature from the device
	#This statement returns a tuple and the humidity, temperature 
	#is defining a tuple
	humidity, temperature = Adafruit_DHT.read_retry(sensor,pin)
	temperature = round(temperature,2)
	#note humidity is not used
	#get date and time
	date = datetime.now().strftime('%Y-%m-%d')
	time = datetime.now().strftime('%H:%M:%S')
	
	#collect the input data for the db into a list
	inputData = (date, time, temperature)
	
	#connect to the db and save data
	db = sqlite3.connect(dBFile)
	cursor = db.cursor()
	#this function is called early to save data on a daily bases (in which case it goes into the daily table,
	#else it goes into the normal table. Default is the normal table
	if table == "tempDaily":
		cursor.execute('''INSERT INTO tempDaily(date,time,temp) VALUES(?,?,?)''',inputData)
	else:
		cursor.execute('''INSERT INTO tempData(date,time,temp) VALUES(?,?,?)''',inputData)
	db.commit()
	db.close()

#write to dailyTemp table at 23:15 each day
targetTime = datetime(2019,10,1,13,0,0)
previousTime = datetime.now()
tempDataFrequency = timedelta(seconds = dataWriteFrequency)
print (tempDataFrequency)
#loop forever	
while True:
	#get and save read to database
	
	#if the current time is greater than the sum of the previous time and the data write frequency than write to 
	#tempData
	if datetime.now() > previousTime + tempDataFrequency:
		print("Write to tempData")
		temperature_db(dBPath,"tempData")
		previousTime = datetime.now()


	#check to see if its time to do the daily temperature write
	#as data is written every 60 seconds there is a possibility
	#that it will miss the daily target i need to find a work
	#around to this
	#I think the way to fix this is to use delta time
	currentTime = datetime.now()
	print(currentTime)
	if currentTime.hour == targetTime.hour and currentTime.minute == targetTime.minute:
		print("DailyTime")
		temperature_db(dBPath, "tempDaily")
		time.sleep(60)
	
	
