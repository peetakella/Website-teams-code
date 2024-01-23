"""
==========================================================================================
Title:          main.py
Authors:        Peter Keller, Jacob Schaef, Simon Swopes
Description:    Entry point for software for the Better Bleeding Control Training Device
Version:        2.0
==========================================================================================
"""

import pygame.mixer
import threading
from queue import Queue

# Top level classes
screen = None
network = None
simulation = None
stateObserver = None
audio = pygame.mixer.init()


#TODO: figure out way to generate events in simulation without importing currently doesn't work


"""
#=================================================================================================
# Seperates simulation object from needing a circular import
def broadCastEvent(state):
    screen._root.event_generate("<<event4>>", state=str(state))

#================================================================================================
# Generates events without circular import
def eventGeneration(blood, data, time):
    screen._root.event_generate("<<event1>>", state=str(blood))
    screen._root.event_generate("<<event2>>", state=str(data))
    screen._root.event_generate("<<event3>>", state=str(time))
"""

# Local Imports
from src.observer import Observer
stateObserver = Observer()
from src.api import *
network = API_Network("http://10.187.243.199:3000")
from src.sim import Simulation
simulation = Simulation(audio)
from src.gui import *


#==================================================================================================
# Program Main function
def main():
    screen.updateWindow()


#==================================================================================================
# Begins multithreading called when osberver state == 4
def simulationBegin(observed_state):

    if observed_state == 4:
        worker = threading.Thread(target= lambda: [simulation.begin()])
        worker.daemon = True
        worker.start()

        
        queueObserver = threading.Thread(target= lambda: [screen.handleQueue()])
        queueObserver.daemon = True
        queueObserver.start()

    screen.updateWindow()




#==================================================================================================
# Start program execution
if __name__ == "__main__":
    screen = Window()
    stateObserver.bind_to(simulationBegin)
    main()
