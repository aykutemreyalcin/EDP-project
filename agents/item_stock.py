from agents.agent import Agent

class ItemStock(Agent):
    def __init__(self, event_manager):
        super().__init__(event_manager)
        self.stock = {}

    def add_item(self, item_name, quantity):
        self.stock[item_name] = self.stock.get(item_name, 0) + quantity
        self.emit_event("item_added", {"item_name": item_name, "quantity": quantity})

    def remove_item(self, item_name, quantity):
        if self.stock.get(item_name, 0) >= quantity:
            self.stock[item_name] -= quantity
            self.emit_event("item_removed", {"item_name": item_name, "quantity": quantity})
        else:
            self.emit_event("stock_insufficient", {"item_name": item_name, "requested": quantity})
