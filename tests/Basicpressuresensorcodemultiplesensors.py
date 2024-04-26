#TE FX29 load cell sensor

#set up digital io
import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
IO.setwarnings(False)           #do not show any warnings
IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
IO.setup(19,IO.OUT)           # initialize GPIO19 as an output, not important for the pressure sensor or load cell
#set up i2c
import time
import smbus2 as smbus
from time import sleep
bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
channel = 1          #select channel

#Condition sensor for continuous measurements
LOAD_SENSOR_ADDRESS1=0x27
LOAD_SENSOR_ADDRESS2=0x26

dummy_command=0x00

offset=1000
global LBS_DATA_SENSOR1,LBS_DATA_SENSOR2

#offset=int((input("Enter offset value, default 1000:") or 1000))                                        #subtracts zero offset per data sheet, should be 1000
LOAD_SENSOR_DATA1=bus.read_byte(LOAD_SENSOR_ADDRESS1)#This apparently turns the load sensor on, only need it once
LOAD_SENSOR_DATA2=bus.read_byte(LOAD_SENSOR_ADDRESS2)#This apparently turns the load sensor on, only need it once
#take continuous measurements and report
while 1:
    global LBS_DATA_SENSOR1,LBS_DATA_SENSOR2
    bus.write_byte(LOAD_SENSOR_ADDRESS1,dummy_command)                                          #without this command, the status bytes go high on every other read
    LOAD_SENSOR_DATA1=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS1,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
    LBS_DATA_SENSOR1=((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000
    print ("Sensor 1 load in lbs:"'{0:.3f}'.format(LBS_DATA_SENSOR1))
    #print ("Sensed load1 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA1[0]&63)*2**8 + LOAD_SENSOR_DATA1[1] - offset)*100/14000), "pounds")#plots out
    
    bus.write_byte(LOAD_SENSOR_ADDRESS2,dummy_command)                                          #without this command, the status bytes go high on every other read
    LOAD_SENSOR_DATA2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS2,dummy_command,2)                                                                                  #It does return the correct two bytes after the initial read byte command
    LBS_DATA_SENSOR2=((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000
    print ("Sensor 2 load in lbs:"'{0:.3f}'.format(LBS_DATA_SENSOR2))
    #print ("Sensed load2 = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA2[0]&63)*2**8 + LOAD_SENSOR_DATA2[1] - offset)*100/14000), "pounds")#plots out    
    
    print ("Average of sensor 1 and 2 in lbs:"'{0:.3f}'.format((LBS_DATA_SENSOR1+LBS_DATA_SENSOR2)/2))
    
    sleep(.1) #have seen some status bits activity with delays less than 1 second, most recent experience is that this delay is u
