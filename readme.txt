How to set the system up.

dependencies

sqlite3 needs to be installed on the system
The python modules for sqlite3, the envirophat HAT (https://shop.pimoroni.com/products/enviro-phathttps://shop.pimoroni.com/products/enviro-phat),
smtplib, sslm, email.mime.text, email.mime.multipart, email.mime.image
matploblib, json, time, os are all needed.

Ensure that a database called temperature_db is created (or a different name
is defined in the main.py and userInput.py scripts)
This database needs a table called tempData, with three coloums date (which is a type Date), time (which is a type Time) and temp (which is a type float)

In main.py and userInput.py the folderPath varaible needs to be the path directory that all the files for the system are stored in.
main.py, clean.py, report.py and db_write.py all need to start up when the device is powered up. The way the writer did this was
by editting /etc/rc.local to run the scripts at start up. Here is an example.....

sudo python /home/pi/repos/temperatureMonitor/main.py &

ensure all the commands include the full path, & at the end, sudo and 
that exit 0 is at the end of the file.

When these are all setup the userInput.py script can be run to define
the user settings.  
