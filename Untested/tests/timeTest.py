"""
=======================================================================================================
Title:          timeTest.py
Author(s):      Simon Swopes
Description:    This is a timed test for the main backend loop. It takes a command line argument
                which is the loops that are timed and the average is then output.
Version:        2.0
======================================================================================================
"""

import sys
import time
import threading
import pygame.mixer
from statistics import stdev

audio = pygame.mixer.init()
from ..src.observer import Observer
stateObserver = Observer()
from ..src.api import *
network = API_Network("http://tosmcoe0005.ttu.edu:3000")
from ..src.sim import Simulation
simulation = Simulation(audio)
from ..src.gui import *
screen = None

def main():
    loopCount = int(sys.argv[-1])
    screen._state = 4

    # No Blood No Sound, Wound = pressure
    simulation.blood = 3
    simulation.sound = 0
    simulation.wound = 3


    backLoopTimes = []

    # intializes sim values
    simulation.runTest()

    for i in range(loopCount):
        backThread = threading.Thread(target = lambda: [simulation.run()])
        backThread.daemon = True
        start = time.perf_counter()
        backThread.start()
        while backThread.is_alive():
            time.sleep(0.0001)

        backLoopTimes.append(time.perf_counter() - start)

    avgBack = sum(backLoopTimes) / loopCount
    
    print("Times:")
    for i in range(loopCount):
        print(f"{backLoopTimes[i]}")

    print(f"\nAverage: {avgBack}")
    print(f"Standard Deviation: {stdev(backLoopTimes)}")

    sys.exit(0)


if __name__ == "__main__":
    screen = Window()
    main()
