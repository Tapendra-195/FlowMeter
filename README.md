# FlowMeter
* main.py -- Main program. Run with sudo privilege for watchdog.
* State.py -- Abstract class for circulation state.
* StartState.py -- Start state implementation for circulation.
* CheckPrimeState.py -- Check prime state implementation for circulation.
* RunningState.py -- Running state implementation for circulation.
* LeakingState.py -- Leaking state implementation for circulation.
* OffState.py -- Off state implementation for circulation.
* Watchdog.py -- Watchdog timer
* RingBuffer.py -- Ring buffer to store events.
* FlowMeter.py -- DFA/FSM to calculate the flow rate at the inlet and the outlet line.
* FlowEvent.py -- Enum containing water circulation events.
* EventGenerator.py -- Generates circulation events by reading inflow and outflow rate at check_interval.
* CirculationSystem.py -- Water Circulation system. Keeps track of Circulation state, handles state transition, and turns the pump on or off.

# Usage
sudo main.py

# Pin Mapping
* Pin 17 -- Inlet flowmeter
* Pin 27 -- Outlet flowmeter
* Pin 20 -- Pump/Chiller realy.
