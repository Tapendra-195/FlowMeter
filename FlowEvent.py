from enum import Enum

class FlowEvent(Enum):
    FLOW_OK = 1
    FLOW_LOW = 2
    LEAK_DETECTED = 3
    OFF = 4
