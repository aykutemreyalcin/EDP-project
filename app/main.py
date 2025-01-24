from flask import Flask, request, render_template
from agents.item_stock import ItemStock
from agents.sales import Sales
from agents.inventory_check import InventoryCheck
from event_manager.event_manager import EventManager

# Initialize Flask app
app = Flask(__name__)

# Create EventManager instance
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

@app.route('/')
def home():
    return render_template('index.html')

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
