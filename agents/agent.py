from abc import ABC, abstractmethod

class Agent(ABC):
    def __init__(self, event_manager):
        self.event_manager = event_manager

    @abstractmethod
    def emit_event(self, event_type, data=None):
        self.event_manager.emit(event_type, data)
