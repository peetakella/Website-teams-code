#Import all neccessary features to code.
import RPi.GPIO as GPIO
import time
from time import sleep
arm = 18
junction = 4
ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
#If code is stopped while the solenoid is active it stays active
#This may produce a warning if the code is restarted and it finds the GPIO Pin, which it defines as non-active in next line, is still active
#from previous time the code was run. This line prevents that warning syntax popping up which if it did would stop the code running.
GPIO.setwarnings(False)
#This means we will refer to the GPIO pins
#by the number directly after the word GPIO. A good Pin Out Resource can be found here https://pinout.xyz/
GPIO.setmode(GPIO.BCM)
#This sets up the GPIO 18 pin as an output pin
GPIO.setup(arm, GPIO.OUT) #arm wound
GPIO.setup(junction, GPIO.OUT) #Junction Wound
while (True):    
    start = time.time()
    #This Turns Relay On. 
    GPIO.output(arm, 1)
    GPIO.output(junction, 1)
    GPIO.output(ENA, GPIO.LOW)
    print('ENA set to LOW - Controller Enabled')
    #Wait .5 Seconds
    sleep(.5)
    #Turns Relay Off. 
    GPIO.output(arm, 0)
    GPIO.output(junction, 0)
    GPIO.output(ENA, GPIO.HIGH)
    print('ENA set to HIGH - Controller Disabled')
    sleep(2) # pause for possible change direction
    #Wait 2 Seconds
    sleep(2)
    finish = time.time()
    cycletime = finish - start
    print (cycletime)
    