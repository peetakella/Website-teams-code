"""
==========================================================================================
Title:          main.py
Authors:        Peter Keller, Jacob Schaef, Simon Swopes
Description:    Entry point for software for the Better Bleeding Control Training Device
Version:        2.0
==========================================================================================
"""
# Library Imports
import pygame.mixer
import threading

# Local Imports
from src.observer import Observer
from src.api import *
from src.sim import Simulation
from src.gui import *

# Global Objects
stateObserver = Observer()
network = API_Network("http://tosmcoe0005.ttu.edu:3000")
simulation = Simulation()
screen = Window()

# Top level classes
screen = None
network = None
simulation = None
stateObserver = None
audio = pygame.mixer.init()


"""
#=================================================================================================
# Seperates simulation object from needing a circular import
def broadCastEvent(state):
    screen._root.event_generate("<<event4>>", state=str(state))"""


#==================================================================================================
# Program Main function
def main():
    stateObserver.bind_to(simulationBegin)
    screen.updateWindow()


#==================================================================================================
# Begins multithreading called when osberver state == 4
def simulationBegin(observed_state):

    if observed_state == 4:
        # Backend Thread
        worker = threading.Thread(target= lambda: [simulation.begin()])
        worker.daemon = True
        worker.start()

        # Observation Thread
        queueObserver = threading.Thread(target= lambda: [screen.handleQueue()])
        queueObserver.daemon = True
        queueObserver.start()

    screen.updateWindow() # Always called when state of window changes




#==================================================================================================
# Start program execution
if __name__ == "__main__":
    main()
