"""
=========================================================================
Title:          events.py
Authors:        Peter Keller, Simon Swopes
Description:    this file contains toplevel event methods
Version:        1.0
=========================================================================
"""

from main import screen, network, simulation

#========================================================================
# Finalization of Data for Network
def end(event4):
    network.submit_TrainingData(simulation.ma_xlist, simulation.timelist, simulation.pressurelist, simulation.blood_loss)
    #TODO stop music
    if event4.state == "0":
        screen._destroy_UpdateState(5)
        return
    
    screen._destroy_UpdateState(6)

