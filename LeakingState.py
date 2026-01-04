import threading
from State import State
from FlowEvent import FlowEvent


class LeakingState(State):
    def __init__(self, timeout_time=5.0):
        self.timeout_time = timeout_time

    def enter(self, system):
        self.timer = threading.Timer(self.timeout_time, self.timeout, args=(system,))
        self.timer.start()


    def handle_event(self, system, event):
        if event == FlowEvent.FLOW_OK:
            system.transition_to(system.runningstate)
        elif event == FlowEvent.OFF:
            system.transition_to(system.offstate)
            
    def timeout(self, system):
        system.transition_to(offstate)
