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

# ItemStock agent: Handles adding/removing items from stock
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

# Sales agent: Handles selling items and reducing stock
class Sales(Agent):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

    def sell_item(self, item_name: str, quantity: int):
        print(f"Processing sale for {quantity} of {item_name}.")
        self.emit_event("item_sold", {"item_name": item_name, "quantity": quantity})

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# InventoryCheck agent: Generates inventory reports
class InventoryCheck(Agent):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

    def generate_report(self, stock):
        print("Generating inventory report:")
        for item, quantity in stock.items():
            print(f"{item}: {quantity}")
        self.emit_event("inventory_report_generated", stock)

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# CustomerRequests agent: Processes customer requests for specific items
class CustomerRequests(Agent):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

    def request_item(self, item_name: str, quantity: int):
        print(f"Customer requests {quantity} of {item_name}.")
        self.emit_event("customer_request", {"item_name": item_name, "quantity": quantity})

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# Event Handler: Listens to and manages events emitted by agents
class EventHandler:
    def __init__(self, event_manager: EventManager, item_stock: ItemStock):
        self.event_manager = event_manager
        self.item_stock = item_stock
        self.subscribe_to_events()

    def subscribe_to_events(self):
        self.event_manager.subscribe("item_added", self.on_item_added)
        self.event_manager.subscribe("item_sold", self.on_item_sold)
        self.event_manager.subscribe("customer_request", self.on_customer_request)
        self.event_manager.subscribe("stock_insufficient", self.on_stock_insufficient)
        self.event_manager.subscribe("inventory_report_generated", self.on_inventory_report_generated)

    def on_item_added(self, data):
        print(f"EventHandler: Item added to stock - {data}")

    def on_item_sold(self, data):
        print(f"EventHandler: Item sold - {data}")
        self.item_stock.remove_item(data["item_name"], data["quantity"])

    def on_customer_request(self, data):
        item_name = data["item_name"]
        quantity = data["quantity"]
        if self.item_stock.stock.get(item_name, 0) >= quantity:
            print(f"EventHandler: Customer request can be fulfilled for {item_name}.")
        else:
            print(f"EventHandler: Not enough stock for {item_name}.")
            self.event_manager.emit("stock_insufficient", {"item_name": item_name, "requested": quantity})

    def on_stock_insufficient(self, data):
        print(f"EventHandler: Insufficient stock for {data['item_name']}. Requested: {data['requested']}.")

    def on_inventory_report_generated(self, data):
        print(f"EventHandler: Inventory report received.")

# Example supermarket EDP system
if __name__ == "__main__":
    # Create an EventManager instance
    event_manager = EventManager()

    # Create agents
    item_stock = ItemStock(event_manager)
    sales = Sales(event_manager)
    inventory_check = InventoryCheck(event_manager)
    customer_requests = CustomerRequests(event_manager)

    # Create EventHandler
    event_handler = EventHandler(event_manager, item_stock)

    # Sequence of events
    print("--- Adding items to stock ---")
    item_stock.add_item("Apples", 50)
    item_stock.add_item("Bananas", 30)

    print("\n--- Customer requests items ---")
    customer_requests.request_item("Apples", 10)

    print("\n--- Selling items ---")
    sales.sell_item("Apples", 10)

    print("\n--- Generating inventory report ---")
    inventory_check.generate_report(item_stock.stock)
