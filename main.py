from abc import ABC, abstractmethod
from typing import Callable, Dict, List

# EventManager to handle subscriptions and event dispatching
class EventManager:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, listener: Callable):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(listener)

    def emit(self, event_type: str, data=None):
        if event_type in self.listeners:
            for listener in self.listeners[event_type]:
                listener(data)

# Abstract base class for agents
class Agent(ABC):
    def __init__(self, event_manager: EventManager):
        self.event_manager = event_manager

    @abstractmethod
    def emit_event(self):
        pass

# ItemStock agent
class ItemStock(Agent):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)
        self.stock = {}

    def add_item(self, item_name: str, quantity: int):
        self.stock[item_name] = self.stock.get(item_name, 0) + quantity
        print(f"Added {quantity} of {item_name} to stock.")
        self.emit_event("item_added", {"item_name": item_name, "quantity": quantity})

    def remove_item(self, item_name: str, quantity: int):
        if self.stock.get(item_name, 0) >= quantity:
            self.stock[item_name] -= quantity
            print(f"Removed {quantity} of {item_name} from stock.")
            self.emit_event("item_removed", {"item_name": item_name, "quantity": quantity})
        else:
            print(f"Not enough {item_name} in stock.")
            self.emit_event("stock_insufficient", {"item_name": item_name, "requested": quantity})

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# Sales agent
class Sales(Agent):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

    def sell_item(self, item_name: str, quantity: int):
        print(f"Processing sale for {quantity} of {item_name}.")
        self.emit_event("item_sold", {"item_name": item_name, "quantity": quantity})

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# InventoryCheck agent
class InventoryCheck(Agent):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

    def check_stock(self, item_name: str):
        print(f"Checking stock for {item_name}.")
        self.emit_event("inventory_checked", {"item_name": item_name})

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# CustomerRequests agent
class CustomerRequests(Agent):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

    def request_item(self, item_name: str, quantity: int):
        print(f"Customer requests {quantity} of {item_name}.")
        self.emit_event("customer_request", {"item_name": item_name, "quantity": quantity})

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# Example usage
if __name__ == "__main__":
    # Create an EventManager instance
    event_manager = EventManager()

    # Create agents
    item_stock = ItemStock(event_manager)
    sales = Sales(event_manager)
    inventory_check = InventoryCheck(event_manager)
    customer_requests = CustomerRequests(event_manager)

    # Define listeners
    def on_item_added(data):
        print(f"Listener: Item added to stock: {data}")

    def on_item_sold(data):
        item_stock.remove_item(data["item_name"], data["quantity"])

    def on_customer_request(data):
        inventory_check.check_stock(data["item_name"])

    # Subscribe listeners to events
    event_manager.subscribe("item_added", on_item_added)
    event_manager.subscribe("item_sold", on_item_sold)
    event_manager.subscribe("customer_request", on_customer_request)

    # Emit events
    item_stock.add_item("Apples", 50)
    customer_requests.request_item("Apples", 10)
    sales.sell_item("Apples", 10)
