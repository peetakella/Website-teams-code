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

# Local Imports
from src.network import *
from src.events import *
from src.gui import Window
from src.simulation import Simulation
from src.observer.py import Observer

# Top level classes
screen = None
network = None
simulation = None
stateObserver = None
audio = pygame.mixer.init()


#==================================================================================================
# Program Main function
def main():
    while True:
        screen.updateWindow()


#==================================================================================================
# Begins multithreading called when osberver state == 4
def simulationBegin(observed_state):
    if observed_state != 4:
        return

    worker = threading.Thread(target=simulation.begin())
    worker.daemon = True
    worker.start()

    

#==================================================================================================
# Start program execution
if __name__ == "__main__":
    network = Network("http://10.187.243.199:3000")
    screen = Window()
    stateObserver = Observer()
    stateObserver.bind_to(simulationBegin)
    simulation = Simulation()
    main()
