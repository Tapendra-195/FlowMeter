from gpiozero import Button
from signal import pause
import time
import sys
from enum import Enum

DEL_TIME = 0.1
    
button = Button(17)



class State(Enum):
    WAIT_FOR_EDGE = 0
    RISING_EDGE_DETECTED = 1
    FALLING_EDGE_DETECTED = 2
    FALLING_EDGE_AT_START = 3
    RISING_EDGE_AFTER_FALLING = 4
    ERROR_STATE = 5




class DFA:
    def __init__(self, Q, Σ, δ, q0, F):
        self.Q = Q   #set of states
        self.Σ = Σ   #set of symbols
        self.δ = δ   #transition function
        self.q0 = q0 #initial state
        self.F = F   #set of final states
        self.speed = 0
        
    def __repr__(self):
        return f"DFA({self.Q},\n\t{self.Σ},\n\t{self.δ},\n\t{self.q0},\n\t{self.F}"

    def run(self, word):
        q = self.q0
        self.speed = 0
        
        while word!="":
            q, y = self.δ[(q,word[0])] #next state, output
            word = word[1:]
            self.speed += y 
        return q in self.F


#String to pass to DFA    
word =""
def add_zero():
    global word
    word +="0"

def add_one():
    global word
    word +="1"


button.when_pressed = add_one
button.when_released = add_zero

#Flow Counter DFA(Deterministic Finite Automata) description
Q = {State.WAIT_FOR_EDGE, State.RISING_EDGE_DETECTED, State.FALLING_EDGE_DETECTED, State.FALLING_EDGE_AT_START, State.RISING_EDGE_AFTER_FALLING, State.ERROR_STATE}
Σ = {"0","1"} #0 for falling edge, 1 for rising edge
δ ={
    (State.WAIT_FOR_EDGE,"0"):(State.FALLING_EDGE_AT_START,0),            (State.WAIT_FOR_EDGE,"1"):(State.RISING_EDGE_DETECTED,0),

    (State.RISING_EDGE_DETECTED,"0"):(State.FALLING_EDGE_DETECTED,1),      (State.RISING_EDGE_DETECTED,"1"):(State.ERROR_STATE,0),
    (State.FALLING_EDGE_DETECTED,"0"):(State.ERROR_STATE,0),               (State.FALLING_EDGE_DETECTED,"1"):(State.RISING_EDGE_DETECTED,1),

    (State.FALLING_EDGE_AT_START,"0"):(State.ERROR_STATE,0),               (State.FALLING_EDGE_AT_START,"1"):(State.RISING_EDGE_AFTER_FALLING,1),
    (State.RISING_EDGE_AFTER_FALLING,"0"):(State.FALLING_EDGE_AT_START,1), (State.RISING_EDGE_AFTER_FALLING,"1"):(State.ERROR_STATE,0),

    (State.ERROR_STATE,"0"):(State.ERROR_STATE,0),                         (State.ERROR_STATE,"1"):(State.ERROR_STATE,0),
}
q0 = State.WAIT_FOR_EDGE
F = Q-{State.ERROR_STATE}

#instance of Flow Counter Automata(or Finite state machine)
flowCounter = DFA(Q, Σ, δ, q0, F)

while True:
    word = ""
    time.sleep(DEL_TIME)
    word_copy = word
    success = flowCounter.run(word_copy)
    if(success):
        print(flowCounter.speed)
        #sys.stdout.write(f"\r{flowCounter.speed}")
    else:
        print("Flowmeter Error state")

