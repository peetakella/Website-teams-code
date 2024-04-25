"""
=======================================================================================
Title:          simulation.py
Authors:        Peter Keller, Jacob Schaef, Simon Swopes
Description:    This is the class that contains all simulation related variables and methods.
Version:        2.0
=======================================================================================
"""
# NOTE: The following are references for the sensors based on the wound type
# These addresses were taken directly from version one they have been hardcoded to allow for speedup
# Version 3 Should break this object down more unfortunately version one was so intertwined that it was not possible to do so for this version
"""
Sensor 1: 0x28 Juntion
Sensor 2: 0x26 Higher arm sensor
Sensor 3: 0x27 Lower arm sensor

dummy_command=0x00
offset=1000
"""

# Library Imports
import RPi.GPIO as GPIO
from time import sleep, perf_counter
from smbus2 import SMBus
from math import log
from queue import Queue
import pygame
from random import shuffle

pygame.mixer.init()

class Simulation:
    # Initializer will eventually take parameters from simulation type`
    def __init__(self):

        self.Config = None

        self.blood = None
        self.wound = None
        self.sound = None
        self.eventIndex = 0
        self.eventQueue = Queue()

        self.timelist = []
        self.pressurelist = []
        self.ma_xlist = []
        self.blood_loss = []
        self.P = True                   # P: "Program Running"
        self.timetostopthebleed = 5     # in seconds


        self.MAX_MOTOR_SPEED = 12000    # Initialize with default value
        self.LOAD_SENSOR_DATA = None
        self.LBS_DATA_SENSOR = None
        self.SENSOR_ADDRESS = None


        self.upthreshold = 20
        self.errorthreshold = 40
        self.STB_timer = 0
        self.cycletime = 0


        self.DATA = None
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []
        self.Hz = 0
        self.ratio = 0

        self.PUL = 12  # pwm pin
        self.DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
        self.ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable).

        self.arm = 18
        self.junction = 4 
        self.p = None

        self.tic1 = None
        self.tic3 = 0
        self.tic4 = None
        self.tic5 = None
        self.totaltime = 0

        self.BloodLost = 0

        self.bus = None

        self.pSound = False
        self.moanIdx = 0
        self.presIdx = 0
        self.moanSounds = ["assets/sounds/Moan1.mp3", "assets/sounds/Moan2.mp3", "assets/sounds/Moan3.mp3"]
        self.presSounds = ["assets/sounds/30secondscream.mp3", "assets/sounds/scream3.mp3", "assets/sounds/getofflong.mp3"]
        self.pLength = len(self.presSounds)
        self.mLength = len(self.moanSounds)

        self.sensorCalibration = 1

        self.filename = None


    #========================================================================
    # Method to clean sim obj at end
    def clean(self):

        self.stop_pump()
        GPIO.cleanup()
        self.bus.close()
        pygame.mixer.music.stop()

        # Update Config file
        self.Config["guestfilesSaved"] += 1
        newConfig = ""
        for key, value in self.Config.items():
            newConfig += f"{key}={value}\n"
        with open("src/config", "w") as file:
            file.write(newConfig)
        sleep(1)
        self.P = False
        quit()

    #========================================================================
    # begin - preprocessing then simulation cycle start optimization hear will only speedup intial load time
    def begin(self):

        # Top is simply just resetting in case of previous trial
        self.eventIndex = 0
        
        if not self.eventQueue.empty():
            self.eventQueue.clear()

        self.timelist = []
        self.pressurelist = []
        self.ma_xlist = []
        self.blood_loss = []
        self.P = True                   # P: "Program Running"


        self.MAX_MOTOR_SPEED = 12000    # Initialize with default value 

        self.DATA = None
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []
        self.Hz = 0
        self.ratio = 0
 
        self.p = None

        self.tic1 = None
        self.tic3 = 0
        self.tic4 = None
        self.tic5 = None
        self.totaltime = 0

        self.errorthreshold = 40
        self.STB_timer = 0
        self.cycletime = 0

        self.BloodLost = 0

        #Shuffle sound Lists
        shuffle(self.moanSounds)
        shuffle(self.presSounds)

        # Check setting and give to sim
        self.Config= {
            "packing_sensor": None,
            "pressure_sensor": None,
            "tourniquet_sensor": None,
            "guestfilesSaved": None,
            "guestMax": None,
        }
        with open("src/config", "r") as file:
            for line in file:
                key, value = line.split("=")
                self.Config[key] = float(value)

        if self.Config["guestfilesSaved"] >= self.Config["guestMax"]:
            self.config["guestfilesSaved"] = 0
            with open("src/config", "w") as file:
                for key, value in self.Config.items():
                    file.write(f"{key}={value}\n")
                    self.Config[key] = float(value)
            self.Config["guestfilesSaved"] = int(self.Config["guestfilesSaved"])
            self.Config["guestMax"] = int(self.Config["guestMax"])

        #========================================================================
        # End of reset

        trainingType = "Packing" if self.wound == 1 else "Tourniquet" if self.wound == 2 else "Pressure"
        # TODO: change to the user name
        self.filename = (f"Trials/{trainingType}/GuestTrial_{self.Config['guestfilesSaved']+1}.txt")
        
        self.tic1 = perf_counter()

        if self.blood == 1:                   #2:30 also known as high
            self.MAX_MOTOR_SPEED = 14000
        if self.blood == 2:                   #5:00 also known as low
            self.MAX_MOTOR_SPEED = 2500

        if self.wound == 3: self.errorthreshold = 70

        
        # Packing = 1, Tourniquet = 2, Pressure = 3
        self.sensorCalibration = self.Config["packing_sensor"] if self.wound == 1 else self.Config["tourniquet_sensor"] if self.wound == 2 else self.Config["pressure_sensor"]

        self.ratio = (self.MAX_MOTOR_SPEED - 100) / (self.upthreshold - 0)

        if self.bus:
            self.bus.close()                        # Remove this line to break the program I dare you, you wont even notice at first
        self.bus = SMBus(1)                         #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
        sleep(1)                                    # This sleep prevents io error
           
        #set up digital io
        GPIO.setwarnings(False)                     #do not show any warnings
        GPIO.setmode (GPIO.BCM)                     #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
        GPIO.setup(19,GPIO.OUT)                     # initialize GPIO19 as an output, not important for the pressure sensor or load cell

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PUL, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.arm, GPIO.OUT)
        GPIO.setup(self.junction, GPIO.OUT)
        if not self.p:
            self.p=GPIO.PWM(self.PUL, 100) #PWM Function is defined can only be initalized once


        self.SENSOR_ADDRESS = 0x28 if self.wound == 1 else 0x26 if self.wound == 2 else 0x27


        # TODO Currently this is throwing an error
        self.LOAD_SENSOR_DATA = self.bus.read_byte(self.SENSOR_ADDRESS)
 
        self.LBS_DATA_SENSOR=0

        # Run Simulation
        while self.P:
            self.run()
        else:
            self.clean()

    #========================================================================
    # Method to run simulation
    # This method is called continuously this is the main cycle for simulation backend
    def run(self):
        self.__collect_Data()
        self.__process_Data()
        self.__setMotorHz()
        self.__motor_UpdatePWM()
        self.__timeTracking()
        self.__calculateBloodLoss()
        self.__checkEnd()
        self.__storeData()
        self.__playSound()
        self.__GUIDataPass()

    #========================================================================
    # Unfortunatly the testing module required a slightly different run initialization
    def runTest(self):
        self.tic1 = perf_counter()

        if self.blood == 1:                   #2:30 also known as high
            self.MAX_MOTOR_SPEED = 14000
        if self.blood == 2:                   #5:00 also known as low
            self.MAX_MOTOR_SPEED = 2500

        if self.wound == 3: self.errorthreshold = 70

        self.ratio = (self.MAX_MOTOR_SPEED - 100) / (self.upthreshold - 0)

        self.bus = SMBus(1)                         #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
           
        #set up digital io
        GPIO.setwarnings(False)                     #do not show any warnings
        GPIO.setmode (GPIO.BCM)                     #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
        GPIO.setup(19,GPIO.OUT)                     # initialize GPIO19 as an output, not important for the pressure sensor or load cell

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PUL, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.arm, GPIO.OUT)
        GPIO.setup(self.junction, GPIO.OUT)
        self.p=GPIO.PWM(self.PUL, 100) #PWM Function is defined
        self.SENSOR_ADDRESS = 0x28 if self.wound == 1 else 0x27 if self.wound == 2 else 0x26

        # Sensor Initialization
        if self.wound == 1:
            self.LOAD_SENSOR_DATA=self.bus.read_byte(0x28)
        elif self.wound == 2:
            self.LOAD_SENSOR_DATA=self.bus.read_byte(0x27)
        elif self.wound == 3:  
            self.LOAD_SENSOR_DATA=self.bus.read_byte(0x26)
        self.LBS_DATA_SENSOR=0

        self.filename = (f"Trials/test.txt")



    #========================================================================
    # Method to stop pump only called once if blood option selected
    def stop_pump(self):
        GPIO.output(self.ENA, GPIO.HIGH)
        GPIO.output(self.junction, 0)
        GPIO.output(self.arm,0)

    #========================================================================
    # Data Collection
    def __collect_Data(self):
        # Attempt to read from sensor 5 tries after that then there is a sensor fault and program will exit
        for i in range(5):
            try :
                self.bus.write_byte(self.SENSOR_ADDRESS, 0x00)  #without this command, the status bytes go high on every other read
                self.LOAD_SENSOR_DATA=self.bus.read_i2c_block_data(self.SENSOR_ADDRESS, 0x00,2)
                break
            except Exception as e:
                if i == 4:
                    print(e)
                    self.clean()


    # Data Processing
    def __process_Data(self):

        # returns correct 2 bytes after inital read
        self.LBS_DATA_SENSOR=((self.LOAD_SENSOR_DATA[0]&63)*2**8 + self.LOAD_SENSOR_DATA[1] - 1000)*100/14000

        self.LBS_DATA_SENSOR = self.sensorCalibration * self.LBS_DATA_SENSOR
        if self.LBS_DATA_SENSOR < 0:
            self.LBS_DATA_SENSOR = 0
        elif self.LBS_DATA_SENSOR > 0 and self.LBS_DATA_SENSOR <= self.upthreshold: 
            self.STB_timer=0
        elif self.LBS_DATA_SENSOR > self.upthreshold and self.LBS_DATA_SENSOR <= self.errorthreshold:
            self.LBS_DATA_SENSOR = self.upthreshold
            self.STB_timer += self.cycletime
        else:
            self.LBS_DATA_SENSOR = 0


    #========================================================================
    # Set Motor Hz
    def __setMotorHz(self):
        self.Hz = -(self.LBS_DATA_SENSOR) * self.ratio + self.MAX_MOTOR_SPEED # Simplified equation for motor Hz


    #========================================================================
    # Motor Update PWM
    def __motor_UpdatePWM(self):
        if self.blood > 2:
            return


        #This Turns Relay On.
        if self.wound == 1:
            GPIO.output(self.junction, 1)
        else:
            GPIO.output(self.arm,1)

        #Motor is Enabled and frequency is set
        self.p.start(50)                        #PWM function is set to duty cycle of 50
        GPIO.output(self.DIR, GPIO.HIGH)        #set Directin to CCW
        GPIO.output(self.ENA, GPIO.LOW)         #enable motor
        self.p.ChangeFrequency(self.Hz)         #Update motor speed to new value of Hz
        self.p.ChangeDutyCycle(50)

    #========================================================================
    # Time Tracking - standard use of using cycle time for calculation of real time
    def __timeTracking(self):
        self.tic4 = self.tic3
        self.tic3 = perf_counter()
        if self.tic4 == 0:
            self.tic4 = self.tic3 - .3
        self.cycletime = self.tic3 - self.tic4
       
        self.tic5 = perf_counter()
        self.totaltime = self.tic5-self.tic1

    #========================================================================
    # Calculate Blood Loss
    def __calculateBloodLoss(self):
        Flow_Rate = 0.2643*log(self.Hz)-1.5221 #Liters per min
        self.BloodLost= self.BloodLost + (self.cycletime * Flow_Rate / 60)

        if self.BloodLost >= 3:
            self.eventQueue.put(False)
            self.clean()


    #========================================================================
    # STB Timer reaches end check
    def __checkEnd(self):
         if self.STB_timer >= self.timetostopthebleed:
            self.eventQueue.put(True)
            self.clean() 

    #========================================================================
    # Store Data
    def __storeData(self):
        self.data1.append(self.totaltime)
        self.data2.append(self.BloodLost)


        self.data3.append(self.LBS_DATA_SENSOR)
        self.DATA = self.LBS_DATA_SENSOR

        with open(self.filename, "a") as file:
            file.write(f"{self.totaltime}\t{self.BloodLost}\t{self.DATA}\n")

    #========================================================================
    # Play Sound
    def __playSound(self):
        if self.sound != 1:
            return

        # Moans or No sound for less than target pressure
        if self.DATA < 20:
            if self.DATA < 10:
                pygame.mixer.music.stop()
            elif not pygame.mixer.music.get_busy() or self.pSound:
                if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
                pygame.mixer.music.load(self.moanSounds[self.moanIdx])
                pygame.mixer.music.play()
                # Cycle through shuffled moan sounds
                self.moanIdx = (self.moanIdx + 1) % self.mLength
            self.pSound = False

        else:
            if not pygame.mixer.music.get_busy() or not self.pSound:
                if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
                pygame.mixer.music.load(self.presSounds[self.presIdx])
                pygame.mixer.music.play()
                # Cycle through shuffled pressure sounds
                self.presIdx = (self.presIdx + 1) % self.pLength
            self.pSound = True
       

    #========================================================================
    # GUI Data Pass
    def __GUIDataPass(self):

        self.blood_loss.append(self.BloodLost)
        self.pressurelist.append(self.DATA)
        self.timelist.append(self.totaltime)
        self.ma_xlist.append(self.upthreshold)

        self.eventQueue.put(self.eventIndex)
        self.eventIndex += 1
        sleep(0.07)
