#TE FX29 load cell sensor

#set up digital io
import RPi.GPIO as IO          #calling header file which helps us use GPIO’s of PI
IO.setwarnings(False)           #do not show any warnings
IO.setmode (IO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
IO.setup(19,IO.OUT)           # initialize GPIO19 as an output, not important for the pressure sensor or load cell

#set up i2c
import sys
import time
import smbus
from time import sleep
#from time import clock
from time import perf_counter
bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
channel = 1          #select channel

#this segment sets up power for the sensor to be controlled by gpio26 so that the instruction to enter
#command mode can follow power up within 6ms. The second sleep command in this segment should be commented and then
#the instruction to enter command mode should immediately follow the relay.on instruction
from gpiozero import LED 
relay = LED(26)
relay.off()
sleep(1)
relay.on()
#sleep(1)

#this segment changes i2c address
LOAD_SENSOR_ADDRESS=0x28 # old address
#i2c write (current address,0xA0,0x00,0x00)    enter command mode
bus.write_i2c_block_data(LOAD_SENSOR_ADDRESS,0xA0,[0x00,0x00])
#i2c write (current address,0x02,0x00,0x00)    command to read eeprom word 2
bus.write_i2c_block_data(LOAD_SENSOR_ADDRESS,0x02,[0x00,0x00])
#i2c read  (current address,0x5A,word2 15:8,word2 7:0) fetch current address
word2=bus.read_i2c_block_data(LOAD_SENSOR_ADDRESS,0x5A,3)
print("word 2 = ", word2)
#relay.off()
sleep(1)

#define new address plus some stuff - 9:3 new address, 12:10 011 - have to figure out what the communication lock is
#very wacky...key is to read 3 bytes, first confirms you've got word2 (0x5A, or 90) the next two bytes include bits 15-13 (000), bits 12-10 (011)
#and then bits 9-3 of the address (currently hex 28, or decimal 40, 0101000) and bits 2-0 (110). I'm going to try to write 0x0D, 0x3E, to get the leading 3
#zeros, the comms lock (011), decimal 39/hex 27 (0100111), plus the trailing 110.
#i2c write (current address,0x42,new address 15:8,new address 7:0)  write new address to eeprom - check C example
NEW_ADDRESS=0x27
bus.write_i2c_block_data(LOAD_SENSOR_ADDRESS,0x42, [0x0D,0x3E])
#i2c write (new address,0x80,0x00,0x00) - exit command mode to normal operating mode
bus.write_i2c_block_data(NEW_ADDRESS, 0x80, [0x00, 0x00])
#sys.exit()

#=========================================================================================================
#Condition sensor for continuous measurements
LOAD_SENSOR_ADDRESS=0x28
NEW_ADDRESS=0x27
dummy_command=0x00
LOAD_SENSOR_DATA=bus.read_byte(NEW_ADDRESS)                                   #This apparently turns the load sensor on, only need it once
offset=int(input("Enter offset, default is 1000") or 1000)
#take continuous measurements and report
while 1:
    
    bus.write_byte(NEW_ADDRESS,0x00)                                          #without this command, the status bytes go high on every other read
    LOAD_SENSOR_DATA=bus.read_i2c_block_data(NEW_ADDRESS,dummy_command,2)     #This should turn the load sensor on, but doesn't.  
                                                                                      #It does return the correct two bytes after the initial read byte command
    
    #print ("Sensed load = ",'{0:.3f}'.format(((LOAD_SENSOR_DATA[0]&63)*2**8 + LOAD_SENSOR_DATA[1] - 1065)*100/14000), "pounds")  #plots output if other
                                                                                                                                  #print statements disabled
    
    '''print ("Raw data, no status:",LOAD_SENSOR_DATA)                                    #returns the two data bytes
    print ("status bits:        ", LOAD_SENSOR_DATA[0]&192)                            #returns the status bits, high order bits in the high order byte
    print ("Sensed load =       ",'{0:.3f}'.format(((LOAD_SENSOR_DATA[0]&63)*2**8 + LOAD_SENSOR_DATA[1] - offset)*100/14000), "pounds")#strips off the status bits in the high order byte,
                                                                                                    #weights the high order byte and adds the low order byte,
                                                                                                   #subtracts off the dead zone, normalizes to 100 pound range
    print()'''
    print ("Sensed load =       ",'{0:.3f}'.format(((LOAD_SENSOR_DATA[0]&63)*2**8 + LOAD_SENSOR_DATA[1] - offset)*100/14000), "pounds")
    sleep(.1) #have seen some status bits activity with delays less than 1 second, most recent experience is that this delay is unnecessary
