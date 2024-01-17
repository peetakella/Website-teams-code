"""
============================================================================================
Title:          observer.py
Author:         Simon Swopes
Description:    implementation of the observer pattern. subject is state of window in GUI class
version:        0.1
============================================================================================
"""

from ..main import screen, simulation

class Observer:
    def __init__(self):
        self._state = screen._state
        self._observers = []

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

        for callback in self._observers:
            callback(new_state)

    def bind_to(self, callback):
        self._observers.append(callback)

