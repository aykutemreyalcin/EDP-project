from flask import Flask, request, render_template_string
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
        self.emit_event("item_added", {"item_name": item_name, "quantity": quantity})

    def remove_item(self, item_name: str, quantity: int):
        if self.stock.get(item_name, 0) >= quantity:
            self.stock[item_name] -= quantity
            self.emit_event("item_removed", {"item_name": item_name, "quantity": quantity})
        else:
            self.emit_event("stock_insufficient", {"item_name": item_name, "requested": quantity})

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# Sales agent: Handles selling items and reducing stock
class Sales(Agent):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

    def sell_item(self, item_name: str, quantity: int):
        self.emit_event("item_sold", {"item_name": item_name, "quantity": quantity})

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# InventoryCheck agent: Generates inventory reports
class InventoryCheck(Agent):
    def __init__(self, event_manager: EventManager):
        super().__init__(event_manager)

    def generate_report(self, stock):
        report = "Inventory Report:\n" + "\n".join([f"{item}: {quantity}" for item, quantity in stock.items()])
        self.emit_event("inventory_report_generated", report)

    def emit_event(self, event_type: str, data=None):
        self.event_manager.emit(event_type, data)

# Flask app setup
app = Flask(__name__)

# Create an EventManager instance
event_manager = EventManager()

# Create agents
item_stock = ItemStock(event_manager)
sales = Sales(event_manager)
inventory_check = InventoryCheck(event_manager)

# Define listeners
def on_item_added(data):
    print(f"Item added: {data}")

def on_item_sold(data):
    item_stock.remove_item(data["item_name"], data["quantity"])
    print(f"Item sold: {data}")

def on_inventory_report_generated(data):
    print(data)

# Subscribe listeners to events
event_manager.subscribe("item_added", on_item_added)
event_manager.subscribe("item_sold", on_item_sold)
event_manager.subscribe("inventory_report_generated", on_inventory_report_generated)

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Supermarket System</title>
</head>
<body>
    <h1>Supermarket Management System</h1>

    <h2>Add Item to Stock</h2>
    <form method="post" action="/add_item">
        <label>Item Name:</label>
        <input type="text" name="item_name" required><br>
        <label>Quantity:</label>
        <input type="number" name="quantity" required><br>
        <button type="submit">Add Item</button>
    </form>

    <h2>Sell Item</h2>
    <form method="post" action="/sell_item">
        <label>Item Name:</label>
        <input type="text" name="item_name" required><br>
        <label>Quantity:</label>
        <input type="number" name="quantity" required><br>
        <button type="submit">Sell Item</button>
    </form>

    <h2>Check Inventory</h2>
    <form method="post" action="/check_inventory">
        <button type="submit">Generate Inventory Report</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/add_item', methods=['POST'])
def add_item():
    item_name = request.form['item_name']
    quantity = int(request.form['quantity'])
    item_stock.add_item(item_name, quantity)
    return "Item added successfully! <a href='/'>Go back</a>"

@app.route('/sell_item', methods=['POST'])
def sell_item():
    item_name = request.form['item_name']
    quantity = int(request.form['quantity'])
    sales.sell_item(item_name, quantity)
    return "Item sold successfully! <a href='/'>Go back</a>"

@app.route('/check_inventory', methods=['POST'])
def check_inventory():
    inventory_check.generate_report(item_stock.stock)
    return "Inventory report generated! Check the console for details. <a href='/'>Go back</a>"

if __name__ == "__main__":
    app.run(debug=True)
