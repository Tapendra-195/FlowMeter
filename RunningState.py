import threading
from State import State
from FlowEvent import FlowEvent

class RunningState(State):
    def enter(self, system):
        #do nothing
        pass
        
    def handle_event(self, system, event):
        if event == FlowEvent.FLOW_LOW:
            system.transition_to(system.checkprimestate)
        elif event == FlowEvent.LEAK_DETECTED:
            system.transition_to(system.leakingstate)
        elif event == FlowEvent.OFF:
            system.transition_to(system.offstatestate)
