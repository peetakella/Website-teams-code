"""
============================================================================================
Title:          observer.py
Author:         Simon Swopes
Description:    implementation of the observer pattern. subject is state of window in GUI class
version:        0.1
============================================================================================
"""

class Observer:
    def __init__(self):
        self._state = 1
        self._observers = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

        if self._observers:
            self._observers(new_state)

    def bind_to(self, callback):
        self._observers = callback

