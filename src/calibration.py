"""
============================================================================================================
Title:          calibration.py
Author(s):      Simon Swopes
Description:    This script is used for reading sensors for calibartion purposes.
Version:        1.0
============================================================================================================
"""

# Import the necessary libraries
import RPi.GPIO as GPIO
from smbus2 import SMBus
from time import sleep
from queue import Queue

# Class for reading and passing sensor data
class Calibration:
    def __init__(self):
        self.SENSOR_ADDRESS = None # Set by Front
        self.sensorValues = [] 
        self.offSet = None # Set by Front
        self.eventQueue = Queue()
        self.LBS_DATA_SENSOR = 0
        self.LOAD_SENSOR_DATA = None
        self.P = True
        self.bus = None
        self.errorthreshold = 40
        self.upThreshold = 20 

        self.newOffset = None

        self.PUL = 12
        self.DIR = 27
        self.ENA = 22

        self.arm = 18
        self.junction = 4

        self.idx = 0
        

    def begin(self):
        if self.bus:
            self.bus.close()
        self.bus = SMBus(1)
        sleep(1)

        # Set up Digital IO
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.OUT)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PUL, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.arm, GPIO.OUT)
        GPIO.setup(self.junction, GPIO.IN)

        self.LOAD_SENSOR_DATA = self.bus.read_byte(self.SENSOR_ADDRESS)

        while self.P:
            self.run()
        self.end()
     
    def end(self):
        GPIO.cleanup()
        self.bus.close()
        self.sensorValues = []
        self.idx = 0
        sleep(1)
        self.P = False

    def run(self):
        self.__collectData()
        self.__processData()
        self.__returnData()

    def __collectData(self):
        for i in range(5):
            try:
                self.bus.write_byte(self.SENSOR_ADDRESS, 0x00)
                self.LOAD_SENSOR_DATA = self.bus.read_i2c_block_data(self.SENSOR_ADDRESS, 0x00, 2)
                break
            except Exception as e:
                if i == 4:
                    print(e)
                    self.end()

    def __processData(self):
        self.LBS_DATA_SENSOR=((self.LOAD_SENSOR_DATA[0]&63)*2**8 + self.LOAD_SENSOR_DATA[1] - 1000)*100/14000

        self.LBS_DATA_SENSOR = self.offSet * self.LBS_DATA_SENSOR

        if self.LBS_DATA_SENSOR < 0:
            self.LBS_DATA_SENSOR = 0
        elif self.LBS_DATA_SENSOR > 0 and self.LBS_DATA_SENSOR <= self.upThreshold:
            self.LBS_DATA_SENSOR = self.LBS_DATA_SENSOR
        elif self.LBS_DATA_SENSOR > self.upThreshold and self.LBS_DATA_SENSOR <= self.errorthreshold:
            self.LBS_DATA_SENSOR = self.upThreshold
        else:
            self.LBS_DATA_SENSOR = 0

    def __returnData(self):
        self.sensorValues.append(self.LBS_DATA_SENSOR)
        self.eventQueue.put(self.idx)
        self.idx += 1
        
        if self.newOffset != None:
            self.offSet = self.newOffset
            self.newOffset = None

        sleep(0.05)
