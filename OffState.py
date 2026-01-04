import threading
from State import State
from FlowEvent import FlowEvent


class OffState(State):
    def enter(self, system):
        system.off() #Turn the pump and the chiller off
               
    def handle_event(self, system, event):
        #could have on event, but i am not adding it
        #ignores all events, need to restart the program to turn on
        pass
