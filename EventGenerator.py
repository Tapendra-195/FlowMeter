import threading
import time
from FlowMeter import Flowmeter
from RingBuffer import RingBuffer
from FlowEvent import FlowEvent

class EventGenerator(threading.Thread):
    def __init__(self, buffer, check_interval=1.0, leak_threshold = 3, flow_threshold = 10):
        super().__init__()
        self.buffer = buffer
        self.check_interval = check_interval
        self.leak_threshold = leak_threshold
        self.flow_threshold = flow_threshold
        self.running = True
        self.flm_in = Flowmeter(17, check_interval) #inlet flowmeter
        self.flm_out = Flowmeter(27, check_interval) #outlet flowmeter
        self.flm_in.start()
        self.flm_out.start()
        

        
    def read_flows(self):
        # Replace with real sensor reads
        in_flow = self.flm_in.get_flow_rate()
        out_flow = self.flm_out.get_flow_rate()

        return in_flow, out_flow

    def generate_event(self):
        in_flow, out_flow = self.read_flows()
        if in_flow - out_flow > self.leak_threshold:
            return FlowEvent.LEAK_DETECTED
        elif in_flow < out_flow:
            print("inflow is smaller than out flow, check wiring.")
            return FlowEvent.OFF #inflow can't be less than out flow
        elif in_flow < self.flow_threshold:
            return FlowEvent.FLOW_LOW
        else:
            return FlowEvent.FLOW_OK

    def run(self):
        while self.running:
            event = self.generate_event()
            self.buffer.push(event)
            time.sleep(self.check_interval)

    def stop(self):
        self.running = False
        self.flm_in.stop()
        self.flm_out.stop()
        
