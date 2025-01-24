from agents.agent import Agent

class Sales(Agent):
    def __init__(self, event_manager):
        super().__init__(event_manager)

    def sell_item(self, item_name, quantity):
        self.emit_event("item_sold", {"item_name": item_name, "quantity": quantity})
