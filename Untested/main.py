"""
==========================================================================================
Title:          main.py
Authors:        Peter Keller, Jacob Schaef, Simon Swopes
Description:    Entry point for software for the Better Bleeding Control Training Device
Version:        2.0
==========================================================================================
"""

import pygame.mixer

# Local Imports
from src.network import *
from src.events import *
from src.gui import Window
from src.simulation import Simulation

# Top level classes
screen = None
network = None
simulation = None
audio = pygame.mixer.init()

#==================================================================================================
# Program Main function
def main():
    while True:
        screen.updateWindow()


#==================================================================================================
# Start program execution
if __name__ == "__main__":
    network = Network("http://10.187.243.199:3000")
    screen = Window()
    simulation = Simulation()
    main()
