"""
=======================================================================================
Title:          simulation.py
Authors:        Peter Keller, Jacob Schaef, Simon Swopes
Description:    This is the class that contains all simulation related variables and methods.
Version:        2.0
=======================================================================================
"""

#NOTE: Currently this class has some repeated proerpty definition along variables
# As refactoring continues this should be cleaned

import RPi.GPIO as GPIO
import time
import smbus
import math
from queue import Queue


sound1 = "/home/stopthebleed/StoptheBleed/Sounds/30seccondscream.mp3"
sound2 = "/home/stopthebleed/StoptheBleed/Sounds/30seccondscream.mp3"
sound3 = "/home/stopthebleed/StoptheBleed/Sounds/30seccondscream.mp3"
timestamp2 = 0
Falloffcount = 0
soundtimer = 0

class Simulation:
    # Initializer will eventually take parameters from simulation type`
    def __init__(self, audio):

        self.audio = audio
        self.blood = None
        self.wound = None
        self.sound = None
        self.eventQueue = Queue()

        self.timelist = []
        self.pressurelist = []
        self.ma_xlist = []
        self.blood_loss = []
        self.P = True # P is for "Program Running"
        self.timetostopthebleed = 1


        self.MAX_MOTOR_SPEED = 12000 # Initialize with default value
        self.LOAD_SENSOR_DATA = None
        self.LBS_DATA_SENSOR = None
        self.SENSOR_ADDRESS = None


        self.upthreshold = 20
        self.errorthreshold = 40
        self.running_max = 0
        self.STB_timer = 0
        self.cycletime = 0


        self.DATA = None
        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []
        self.Hz = 0
        self.ratio = 0

        self.PUL = 12  #pwm pin
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

        #TODO Throw error codes for when and if there is something that can't be in a file name and have them try again
        self.filename = (f"A - Previous Trial.txt")

    #========================================================================
    # Method to begin simulation
    def begin(self):
        # NOTE: as refactoring continues may need to make variables class properties instead

        


        #tic3 = 0 #timestamp

        self.tic1 = time.perf_counter()

        if self.blood.get() == 1:     #2:30 also known as high
            self.MAX_MOTOR_SPEED = 14000
        if self.blood.get() == 2:     #5:00 also known as low
            self.MAX_MOTOR_SPEED = 2500

        if self.wound.get() == 3: self.errorthreshold = 70


        # for reference
        """ #Motor speed value is set
        input_min = 0
        input_max1 = upthreshold1
        input_max2 = upthreshold2
        input_max3 = upthreshold3
        output_min = 100 #frequency in hz, higher is faster pumping
        output_max = MAX_MOTOR_SPEED"""

        self.ratio = (self.MAX_MOTOR_SPEED - 100) / (self.upthreshold - 0)

        #BloodLost = 0
        self.bus = smbus.SMBus(1) #I2C channel 1 is connected to the GPIO pins 2 (SDA) and 4 (SCL)
           
        channel = 1          #select channel
        #set up digital io
        GPIO.setwarnings(False)           #do not show any warnings
        GPIO.setmode (GPIO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as ‘GPIO19’)
        GPIO.setup(19,GPIO.OUT)       # initialize GPIO19 as an output, not important for the pressure sensor or load cell

        """ PUL = 12  #pwm pin
        DIR = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
        ENA = 22  # Controller Enable Bit (High to Enable / LOW to Disable)."""

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PUL, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        """arm = 18
        junction = 4  """  
        GPIO.setup(self.arm, GPIO.OUT)
        GPIO.setup(self.junction, GPIO.OUT)
        self.p=GPIO.PWM(self.PUL, 100) #PWM Function is defined

        #Condition sensor for continuous measurements
        # These are just for reference
        """LOAD_SENSOR_ADDRESS1=0x28 #junction
        LOAD_SENSOR_ADDRESS2=0x27 #Higher arm sensor
        LOAD_SENSOR_ADDRESS3=0x26 #Lower arm sensor
        dummy_command=0x00
        offset=1000"""

        self.SENSOR_ADDRESS = 0x28 if self.wound.get() == 1 else 0x27 if self.wound.get() == 2 else 0x26

        if self.wound.get() == 1:
            self.LOAD_SENSOR_DATA=self.bus.read_byte(0x28)#This apparently turns the load sensor on, only need it once
        elif self.wound.get() == 2:
            self.LOAD_SENSOR_DATA=self.bus.read_byte(0x27)
        elif self.wound.get() == 3:  
            self.LOAD_SENSOR_DATA=self.bus.read_byte(0x26)
        self.LBS_DATA_SENSOR=0

        # Run Simulation
        while self.P:
            self.run()

    #========================================================================
    # NOTE: primary method
    # Method to run simulation
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
    # Method to stop pump
    def stop_pump(self):
        GPIO.output(self.ENA, GPIO.HIGH)
        GPIO.output(self.junction, 0)
        GPIO.output(self.arm,0)

    #========================================================================
    # Data Collection
    def __collect_Data(self):
        time.sleep(0.01)
        
        try :
            self.bus.write_byte(self.SENSOR_ADDRESS, 0x00)#without this command, the status bytes go high on every other read
            self.LOAD_SENSOR_DATA=self.bus.read_i2c_block_data(self.SENSOR_ADDRESS, 0x00,2)     #This should turn the load sensor on, but doesn't.  
        except OSError:
            #time.sleep(0.001)
               
            try :
                self.LOAD_SENSOR_DATA=self.bus.read_i2c_block_data(self.SENSOR_ADDRESS, 0x00,2)     #This should turn the load sensor on, but doesn't.  
            except OSError:
                #time.sleep(0.001)
                   
                try :
                    self.LOAD_SENSOR_DATA=self.bus.read_i2c_block_data(self.SENSOR_ADDRESS, 0x00,2)     #This should turn the load sensor on, but doesn't.  
                except OSError:
                    #time.sleep(0.001)
               
                    try :
                        self.LOAD_SENSOR_DATA=self.bus.read_i2c_block_data(self.SENSOR_ADDRESS, 0x00,2)     #This should turn the load sensor on, but doesn't.  
                    except OSError:
                        #time.sleep(0.001)
                           
                        try :
                            self.LOAD_SENSOR_DATA=self.bus.read_i2c_block_data(self.SENSOR_ADDRESS, 0x00,2)     #This should turn the load sensor on, but doesn't.  
                        except OSError:
                            self.stop_pump()
                            self.P = False
                            #time.sleep(0.001)
                            quit()

                           
   

    #========================================================================
    # Data Processing
    def __process_Data(self):

        self.LBS_DATA_SENSOR=((self.LOAD_SENSOR_DATA[0]&63)*2**8 + self.LOAD_SENSOR_DATA[1] - 1000)*100/14000 #It does return the correct two bytes after the initial read byte command

        self.LBS_DATA_SENSOR = 1 * self.LBS_DATA_SENSOR #TODO: is this necessary?
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
        self.Hz = -(self.LBS_DATA_SENSOR) * self.ratio + self.MAX_MOTOR_SPEED


    #========================================================================
    # Motor Update PWM
    def __motor_UpdatePWM(self):
        if self.blood.get() > 2:
            return


        #This Turns Relay On.
        if self.wound.get() == 1:
            GPIO.output(self.junction, 1)
        else:
            GPIO.output(self.arm,1)

        #Motor is Enabled and frequency is set
        self.p.start(50) #PWM function is set to duty cycle of 50
        GPIO.output(self.DIR, GPIO.HIGH)      #set Directin to CCW
        GPIO.output(self.ENA, GPIO.LOW)  #enable motor
        self.p.ChangeFrequency(self.Hz)            #Update motor speed to new value of Hz
        self.p.ChangeDutyCycle(50)

    #========================================================================
    # Time Tracking
    def __timeTracking(self):
        self.tic4 = self.tic3
        self.tic3 = time.perf_counter()
        if self.tic4 == 0:
            self.tic4 = self.tic3 - .3
        self.cycletime = self.tic3 - self.tic4
       
        self.tic5 = time.perf_counter()
        self.totaltime = self.tic5-self.tic1

    #========================================================================
    # Calculate Blood Loss
    def __calculateBloodLoss(self):
        Flow_Rate = 0.2643*math.log(self.Hz)-1.5221 #Liters per min
        self.BloodLost= self.BloodLost + (self.cycletime * Flow_Rate / 60)

        if self.BloodLost >= 3:
            self.stop_pump()
            self.broadCastEvent(0)
            #time.sleep(0.001)
            #quit() #TODO end thread and go back to home


    #========================================================================
    # STB Timer reaches end check
    def __checkEnd(self):
         if self.STB_timer >= self.timetostopthebleed:
            self.stop_pump()
            broadCastEvent(1)
            self.P = False
            #time.sleep(0.001)
            quit()

    #========================================================================
    # Store Data
    def __storeData(self):
        self.data1.append(self.totaltime)
        self.data2.append(self.BloodLost)


        self.data3.append(self.LBS_DATA_SENSOR)
        self.DATA = self.LBS_DATA_SENSOR

        # TODO: change to doing this once at end of simulation by configuring lists
        with open(self.filename, "a") as file:
            file.write(f"{self.totaltime}\t{self.BloodLost}\t{self.DATA}\n")

    #========================================================================
    # Play Sound
    def __playSound(self):
        if self.sound.get() != 1:
            return

        global timestamp2, Falloffcount, soundtimer
        timestamp1 = time.perf_counter()
        if timestamp2 == 0:
            timestamp1 = timestamp2

        soundtimer = timestamp1-timestamp2
        if self.DATA >= 20 and soundtimer == 0:
            timestamp2 = time.perf_counter()
            if Falloffcount in [0,3,6,9,12]:
                self.audio.music.stop()
                self.audio.music.load("/home/stopthebleed/StoptheBleed/Sounds/30seccondscream.mp3")
                self.audio.music.set_volume(1.0)
                self.audio.music.play()                    
                   
            elif Falloffcount in [1,4,7,10,13]:
                self.audio.music.stop()
                self.audio.music.load("/home/stopthebleed/StoptheBleed/Sounds/scream3.mp3")
                self.audio.music.set_volume(1.0)
                self.audio.music.play()
                 
            else:
                self.audio.music.stop()
                self.audio.music.load("/home/stopthebleed/StoptheBleed/Sounds/getofflong.mp3")
                self.audio.music.set_volume(1.0)
                self.audio.music.play()
                   
        if self.DATA < 20 and self.DATA > 10 and soundtimer != 0:

            Falloffcount += 1
            self.audio.music.stop()
            self.audio.music.load("/home/stopthebleed/StoptheBleed/Sounds/Moan1.mp3")
            self.audio.music.set_volume(0.5)
            self.audio.music.play()
            timestamp2 = 0
           
        if self.DATA < 10 :
            self.audio.music.stop()

    #========================================================================
    # GUI Data Pass
    def __GUIDataPass(self):
        rounded_BloodLost = round(self.BloodLost, 6)  # Rounds to 8 decimal places#TODO make string
        big_bloodLost = rounded_BloodLost*1000000
        int_BloodLost = int(big_bloodLost)
       
        rounded_totaltime = round(self.totaltime, 6)  # Rounds to 8 decimal places
        big_totaltime = rounded_totaltime*1000000
        int_totaltime = int(big_totaltime)
       
        rounded_DATA = round(self.DATA, 6)  # Rounds to 8 decimal places
        big_DATA = rounded_DATA*1000000
        int_DATA = int(big_DATA)
       
        
        self.eventQueue.put([int_BloodLost, int_DATA, int_totaltime])
        time.sleep(0.01)
