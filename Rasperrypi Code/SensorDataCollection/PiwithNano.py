import serial
import time
import csv
import datetime
from time import localtime, strftime
import os

i = 1
while os.path.exists("/home/pi/Data/Mission_%s.csv" % i):
    i += 1

ser = serial.Serial('/dev/ttyUSB1', 9600)
# data to be written row-wise in csv fil 
data = [['Time', 'Distance', 'GPS', 'Temperature']] 
  
# opening the csv file in 'w' mode 
file = open('/home/pi/Data/Mission_%s.csv' % i, 'w', newline ='') 
  
# writing the data into the file 
with file:     
     write = csv.writer(file) 
     write.writerows(data)

while(1):
    # First Sensor
    # Send the number 1 to the arduino to get sensor 1 data
    ser.write(str.encode('1'))
    # Get the sensor reading from arduino
    number = ser.read()
    # Convert the reading to a number
    real = int.from_bytes(number,byteorder='big')
    print(real)
    
    # Second Sensor
    
    
    # data to be written row-wise in csv fil 
    data = [[strftime("%Y-%m-%d %H:%M:%S", localtime()), real, ' ', ' ']] 
  
    # opening the csv file in 'a' mode 
    file = open('/home/pi/Data/Mission_%s.csv' % i, 'a', newline ='') 
  
    # writing the data into the file 
    with file:     
        write = csv.writer(file) 
        write.writerows(data)
    
    
    time.sleep(1)
    
    
     