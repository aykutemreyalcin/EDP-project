from agents.agent import Agent

class InventoryCheck(Agent):
    def __init__(self, event_manager):
        super().__init__(event_manager)

    def generate_report(self, stock):
        report = "Inventory Report:\n" + "\n".join([f"{item}: {quantity}" for item, quantity in stock.items()])
        self.emit_event("inventory_report_generated", report)
