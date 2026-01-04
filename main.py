from Watchdog import Watchdog
import time
from EventGenerator import EventGenerator
from RingBuffer import RingBuffer
from CirculationSystem import CirculationSystem
from FlowEvent import FlowEvent

#Play with these values and figure out the working one from experiment
leak_threshold = 3 #maximum inflow-outflow threshold
flow_threshold = 10 #minimum acceptable inflow rate
check_interval=1.0 #Flow rate check interval / event generation interval

prime_check_timeout = 5.0 #prime check state timeout time
leak_check_timeout = 5.0 #leak check state timeout time

buffer = RingBuffer(size=20)
generator = EventGenerator(buffer,check_interval, leak_threshold, flow_threshold)
generator.start()

circulation = CirculationSystem(prime_check_timeout, leak_check_timeout)

with Watchdog() as wd:
    # FSM main loop
    try:
        while True:
            event = buffer.pop()
            if event:
                #handle event
                circulation.handle_event(event)
                print("FSM handling:", event)
          
            wd.pet_dog()
    except KeyboardInterrupt:
        circulation.handle_event(FlowEvent.OFF)
        generator.stop()
        generator.join()

        

