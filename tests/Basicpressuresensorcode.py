#TE FX29 load cell sensor

#set up digital io
import RPi.GPIO as GPIO          #calling header file which helps us use GPIO’s of PI
GPIO.setwarnings(False)           #do not show any warnings
GPIO.setmode (GPIO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
GPIO.setup(19,GPIO.OUT)           # initialize GPIO19 as an output, not important for the pressure sensor or load cell
#set up i2c
import time
import smbus
from time import sleep
bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
channel = 1          #select channel

#Condition sensor for continuous measurements
LOAD_SENSOR_ADDRESS=0x26	
dummy_command=0x00
offset=1000
#offset=int((input("Enter offset value, default 1000:") or 1000))                                        #subtracts zero offset per data sheet, should be 1000
LOAD_SENSOR_DATA=bus.read_byte(LOAD_SENSOR_ADDRESS)#This apparently turns the load sensor on, only need it once
print(1)
#take continuous measurements and report
while 1:
    
    bus.write_byte(LOAD_SENSOR_ADDRESS,dummy_command)                                          #without this command, the status bytes go high on every other read
    LOAD_SENSOR_DATA=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                                                                                      #It does return the correct two bytes after the initial read byte command
    print ("Sensed load = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA[0]&63)*2**8 + LOAD_SENSOR_DATA[1] - offset)*100/14000), "pounds")#plots out       

    sleep(.1) #have seen some status bits activity with delays less than 1 second, most recent experience is that this delay is u

