# Supermarket Event-Driven Programming (EDP) System

## Overview
The Supermarket Event-Driven Programming (EDP) System is a Python-based application designed to manage supermarket operations using an event-driven approach. The system includes the following agents:

- **ItemStock**: Handles adding and removing items from stock.
- **Sales**: Manages selling items and reducing stock.
- **InventoryCheck**: Generates inventory reports.
- **CustomerRequests**: Processes customer requests for specific items.

The system is integrated with a Flask-based web interface, allowing users to interact with the system through simple forms and buttons.

## Features
- Event-driven architecture for efficient task handling.
- Real-time stock updates and inventory management.
- User-friendly web interface for customers and staff.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/supermarket-edp.git
   cd supermarket-edp
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:5000`.

## Usage

### Adding Items to Stock
1. Go to the "Add Item to Stock" section on the web interface.
2. Enter the item name and quantity.
3. Click the "Add Item" button to add the item to stock.

### Selling Items
1. Navigate to the "Sell Item" section.
2. Enter the item name and quantity to sell.
3. Click the "Sell Item" button to process the sale.

### Checking Inventory
1. Go to the "Check Inventory" section.
2. Click the "Generate Inventory Report" button.
3. Check the console for the inventory report.

## Example
### Adding and Selling Items
1. Add 50 apples to stock.
2. Sell 10 apples.
3. Generate the inventory report to confirm stock levels.

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Flask for providing a simple and flexible web framework.
- Python for making event-driven programming straightforward and efficient.
