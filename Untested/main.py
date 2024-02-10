"""
==========================================================================================
Title:          main.py
Authors:        Peter Keller, Jacob Schaef, Simon Swopes
Description:    Entry point for software for the Better Bleeding Control Training Device
Version:        2.0
==========================================================================================
"""
"""
Version 2 is a mess. It is a complete rewrite of the original code. The original code was
written as a single file with tons of cross referencing. This version unfortuneatly carried
some of these poor designs over but is a significant improvement. The bulk of the code is broken into three parts:
    - GUI: This is where the application spends most of its time. Written with Tkinter it could be improved and be modularized.
    - Sim: This is the backend of a running simulation. It runs in a separate thread and handles all hardware reads and passes data to the GUI.
    - API: This is the network layer. This object is not used in guest simulations but can communicate with a server on the same network.

There is lots of room for improvement but this is a significant improvement over the original code.
... Good luck
"""

# Library Imports
import threading


# Local Imports (Import and Initializtion order does matter, be wary of circular dependencies)
from src.observer import Observer
stateObserver = Observer()
from src.api import API_Network
network = API_Network("http://tosmcoe0005.ttu.edu:3000")
from src.sim import Simulation
simulation = Simulation()
from src.gui import *
screen = None


#==================================================================================================
# Program Main function
def main():
    screen.updateWindow()


#==================================================================================================
# Begins multithreading called when osberver state == 4
# Misleading name as this is called any time the gui window state changes and this actually updates the window
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
    stateObserver.bind_to(simulationBegin) # The observer object could probably be avoided by initializing the sim from the GUI
    screen = Window()
    main()
