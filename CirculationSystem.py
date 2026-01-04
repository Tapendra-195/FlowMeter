from StartState import StartState
from CheckPrimeState import CheckPrimeState
from RunningState import RunningState
from LeakingState import LeakingState
from OffState import OffState
from EventGenerator import FlowEvent
import RPi.GPIO as GPIO
RELAY_PIN = 20

class CirculationSystem:
    def __init__(self, prime_check_timeout, leak_check_timeout):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAY_PIN, GPIO.OUT)

        self.startstate = StartState()
        self.checkprimestate = CheckPrimeState(prime_check_timeout)
        self.runningstate = RunningState()
        self.leakingstate = LeakingState(leak_check_timeout)
        self.offstate = OffState()
        self.current_state = self.startstate
        self.current_state.enter(self)

        
    def transition_to(self, new_state):
        self.current_state.exit()
        self.current_state = new_state
        self.current_state.enter(self)

    def handle_event(self, event):
        self.current_state.handle_event(self, event)

    def on(self):
        #To be completed, make sure the pin is pulled down to ground to avoid floating pin.
        #turn on the relay
        print("pump on")
        GPIO.output(RELAY_PIN, GPIO.HIGH)  # LED on
        
        
    def off(self):
        print("pump off")
        #turn off the relay
        GPIO.output(RELAY_PIN, GPIO.LOW)  # LED on
