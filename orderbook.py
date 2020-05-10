class Orderbook():
    def __init__(self):
        self.order_history = []
        self.bid_book = {}
        self.ask_book = {}

    def add_order_to_history(self, order):

    def add_order_to_book(self, order):

    def remove_order(self, order_side, order_price, order_id):

    def modify_order(self, order_size, order_quantity, order_id, order_price):

    def add_trade_to_book(self): # Need to add more here

    def confirm_trade(self, timestamp, order_side, order_quantity, order_id, order_price):

    def confirm_modify(self, timestamp, order_side, order_quantity, order_id):

    def process_order(self, order): #this will do most of the work

    def match_trade(self, order):


