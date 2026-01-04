from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def handle_event(self, system, event):
        """Handle an event and optionally change system's state"""
        pass

    @abstractmethod
    def enter(self, system):
        pass

    def exit(self):
        # Cancel timer if still running                                         
        if hasattr(self, "timer"):
            self.timer.cancel()
