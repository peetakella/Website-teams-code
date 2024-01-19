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

# Top level classes
screen = None
network = None
simulation = None
stateObserver = None
audio = pygame.mixer.init()

#=================================================================================================
# Seperates simulation object from needing a circular import
def broadCastEvent(state):
    screen._root.event_generate("<<event4>>", state=str(state))

# Local Imports
from src.observer import Observer
stateObserver = Observer()
from src.api import *
network = API_Network("http://10.187.243.199:3000")
#from src.events import *
from src.gui import *
from src.simulation import Simulation



#==================================================================================================
# Program Main function
def main():
    screen.updateWindow()


#==================================================================================================
# Begins multithreading called when osberver state == 4
def simulationBegin(observed_state):

    screen.updateWindow()

    if observed_state != 4:
        return

    worker = threading.Thread(target=simulation.begin())
    worker.daemon = True
    worker.start()


#==================================================================================================
# Start program execution
if __name__ == "__main__":
    simulation = Simulation()
    screen = Window()
    stateObserver.bind_to(simulationBegin)
    main()
