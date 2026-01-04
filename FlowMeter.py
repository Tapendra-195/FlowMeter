from gpiozero import Button
import time
from enum import Enum
import threading

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






class Flowmeter:
    
    
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

    def __init__(self, pin, interval):
        self._interval = interval
        self._flow_rate = 0.0
        self._success = False
        self._running = False
        self._flowmeter_pin = pin #Pin the signal from the flowmeter is connected to
        self._current_word = "" #Word is a technical term in DFA/FSM
        self._flow_counter = DFA(Flowmeter.Q, Flowmeter.Σ, Flowmeter.δ, Flowmeter.q0, Flowmeter.F)
        self._lock = threading.Lock()
        
    def get_flow_rate(self):
        return self._flow_rate

    def is_success(self):
        return self._success

    def get_current_word(self):
        return self._current_word
    
    def start(self):
        self._flow_sensor = Button(self._flowmeter_pin)
        self._flow_sensor.when_pressed =  lambda: self._append_letter("1")
        self._flow_sensor.when_released =  lambda: self._append_letter("0")
        self._running = True
        self._thread = threading.Thread(target=self._calculate_speed, daemon=True)
        self._thread.start()
        
    def _append_letter(self, letter):
        #Make sure we don't change variable when it is being used somewhere else
        with self._lock:
            self._current_word += letter #letter is also a technical term in DFA/FSM

    def _calculate_speed(self):
        while self._running:
            #Copy the word first so that the interrupt can't modify it
            with self._lock:
                word = self._current_word
                self._current_word = ""
                
            self._success = self._flow_counter.run(word)
            self._flow_rate = self._flow_counter.speed
            time.sleep(self._interval)

    def stop(self):
        self._running = False
        self._thread.join()
        

'''
flm_in = Flowmeter(17) #inlet flowmeter
flm_out = Flowmeter(27) #outlet flowmeter
flm_in.start()
flm_out.start()

while True:
    in_flow = flm_in.get_flow_rate()
    out_flow = flm_out.get_flow_rate()
    print(f"\r in flow = {in_flow} out flow = {out_flow}", end="", flush=True)
    time.sleep(2)
    #print(f"\r current_word = {flm_in.get_current_word()} , {flm_out.get_current_word()}", end="", flush=True)
'''
