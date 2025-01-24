import unittest
from event_manager.event_manager import EventManager

class TestEventManager(unittest.TestCase):
    def test_event_subscription_and_emission(self):
        event_manager = EventManager()
        result = []

        def test_listener(data):
            result.append(data)

        event_manager.subscribe("test_event", test_listener)
        event_manager.emit("test_event", "data_payload")
        
        self.assertIn("data_payload", result)

if __name__ == '__main__':
    unittest.main()
