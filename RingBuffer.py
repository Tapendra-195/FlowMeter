import threading
from collections import deque

class RingBuffer:
    def __init__(self, size=10):
        self.buffer = deque(maxlen=size)
        self.lock = threading.Lock()

    def push(self, item):
        with self.lock:
            self.buffer.append(item)

    def pop(self):
        with self.lock:
            if self.buffer:
                return self.buffer.popleft()
            return None
