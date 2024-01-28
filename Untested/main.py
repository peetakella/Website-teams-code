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
audio = pygame.mixer.init()
from src.observer import Observer
stateObserver = Observer()
from src.api import *
network = API_Network("http://tosmcoe0005.ttu.edu:3000")
from src.sim import Simulation
simulation = Simulation(audio)
from src.gui import *
screen = None


#==================================================================================================
# Program Main function
def main():
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
    stateObserver.bind_to(simulationBegin)
    screen = Window()
    main()
