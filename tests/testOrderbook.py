from project.orderbook import Orderbook

class TestBook:
    def setup_method(self):
        self.test_book = Orderbook()
        self.buy_order_1 = {'order_id': 't1_1', 'timestamp': 2, 'type': 'add', 'quantity': 1, 'side': 'buy', 'price': 50}
        self.buy_order_2 = {'order_id': 't1_2', 'timestamp': 3, 'type': 'add', 'quantity': 1, 'side': 'buy', 'price': 50}
        self.buy_order_3 = {'order_id': 't10_1', 'timestamp': 4, 'type': 'add', 'quantity': 3, 'side': 'buy', 'price': 49}
        self.buy_order_4 = {'order_id': 't11_1', 'timestamp': 5, 'type': 'add', 'quantity': 3, 'side': 'buy', 'price': 47}
        self.sell_order_1 = {'order_id': 't1_3', 'timestamp': 2, 'type': 'add', 'quantity': 1, 'side': 'sell', 'price': 52}
        self.sell_order_2 = {'order_id': 't1_4', 'timestamp': 3, 'type': 'add', 'quantity': 1, 'side': 'sell', 'price': 52}
        self.sell_order_3 = {'order_id': 't10_2', 'timestamp': 4, 'type': 'add', 'quantity': 3, 'side': 'sell', 'price': 53}
        self.sell_order_4 = {'order_id': 't11_2', 'timestamp': 5, 'type': 'add', 'quantity': 3, 'side': 'sell', 'price': 55}

    def test_add_order_to_history(self):
        '''test add_order_to_history()'''
        test_order = {'order_id': 't1_5', 'timestamp': 4, 'type': 'add', 'quantity': 5, 'side': 'sell', 'price': 55}
        assert len(self.test_book.order_history) == 0
        test_order['exid'] = 1
        self.test_book.add_order_to_history(test_order)
        assert test_order == self.test_book.order_history[0]

    def test_add_order_to_book(self):
        '''Add two buy orders, 2 sell to check bid/ask_book and bid/ask_book_prices'''
        assert len(self.test_book.bid_book_prices) == 0
        assert len(self.test_book.bid_book) == 0
        
        self.test_book.add_order_to_book(self.buy_order_1)
        assert 50 in self.test_book.bid_book_prices
        assert 50 in self.test_book.bid_book.keys()
        assert self.test_book.bid_book[50]['num_orders'] == 1
        assert self.test_book.bid_book[50]['size'] == 1
        assert self.test_book.bid_book[50]['order_ids'][0] == self.buy_order_1['order_id']
        
        self.test_book.add_order_to_book(self.buy_order_2)
        assert self.test_book.bid_book[50]['num_orders'] == 2
        assert self.test_book.bid_book[50]['size'] == 2
        assert self.test_book.bid_book[50]['order_ids'][1] == self.buy_order_2['order_id']
        assert self.test_book.bid_book[50]['orders'][self.buy_order_2['order_id']] == self.buy_order_2
     
        assert len(self.test_book.ask_book_prices) == 0
        assert len(self.test_book.ask_book) == 0

        self.test_book.add_order_to_book(self.sell_order_1)
        assert 52 in self.test_book.ask_book_prices
        assert 52 in self.test_book.ask_book.keys()
        assert self.test_book.ask_book[52]['num_orders'] == 1
        assert self.test_book.ask_book[52]['size'] == 1
        assert self.test_book.ask_book[52]['order_ids'][0] == self.sell_order_1['order_id']

        self.test_book.add_order_to_book(self.sell_order_2)
        assert self.test_book.ask_book[52]['num_orders'] == 2
        assert self.test_book.ask_book[52]['size'] == 2
        assert self.test_book.ask_book[52]['order_ids'][1] == self.sell_order_2['order_id']
        assert self.test_book.ask_book[52]['orders'][self.sell_order_2['order_id']] == self.sell_order_2

    def test_remove_order(self):
        self.test_book.add_order_to_book(self.buy_order_1)
        self.test_book.add_order_to_book(self.buy_order_2)
        assert 50 in self.test_book.bid_book_prices
        assert 50 in self.test_book.bid_book.keys()
        assert self.test_book.bid_book[50]['num_orders'] == 2
        assert self.test_book.bid_book[50]['size'] == 2
        assert len(self.test_book.bid_book[50]['order_ids']) == 2

        #try remove order
        self.test_book.remove_order('buy', 50, 't1_1')
        assert self.test_book.bid_book[50]['num_orders'] == 1
        assert self.test_book.bid_book[50]['size'] == 1
        assert len(self.test_book.bid_book) == 1
        assert 't1_1' not in self.test_book.bid_book[50]['orders'].keys()
        assert 50 in self.test_book.bid_book_prices

        #remove 2nd order
        self.test_book.remove_order('buy', 50, 't1_2')
        assert len(self.test_book.bid_book_prices) == 0
        assert self.test_book.bid_book[50]['num_orders'] == 0
        assert self.test_book.bid_book[50]['size'] == 0
        assert len(self.test_book.bid_book[50]['order_ids']) == 0
        assert 't1_2' not in self.test_book.bid_book[50]['orders'].keys()
        assert 50 not in self.test_book.bid_book_prices

        #remove 2nd again
        self.test_book.remove_order('buy', 50, 't1_2')
        assert len(self.test_book.bid_book_prices) == 0
        assert self.test_book.bid_book[50]['num_orders'] == 0
        assert self.test_book.bid_book[50]['size'] == 0
        assert len(self.test_book.bid_book[50]['order_ids']) == 0
        assert 't1_2' not in self.test_book.bid_book[50]['orders'].keys()
        
        #test for ask book
        self.test_book.add_order_to_book(self.sell_order_1)
        self.test_book.add_order_to_book(self.sell_order_2)
        assert 52 in self.test_book.ask_book_prices
        assert 52 in self.test_book.ask_book.keys()
        assert self.test_book.ask_book[52]['num_orders'] == 2
        assert self.test_book.ask_book[52]['size'] == 2
        assert len(self.test_book.ask_book[52]['order_ids']) == 2

        #remove sell_order_1
        self.test_book.remove_order('sell', 52, 't1_3')
        assert self.test_book.ask_book[52]['num_orders'] == 1
        assert self.test_book.ask_book[52]['size'] == 1
        assert len(self.test_book.ask_book[52]['order_ids']) == 1
        assert 't1_3' not in self.test_book.ask_book[52]['orders'].keys()
        assert 52 in self.test_book.ask_book_prices

        #remove 2nd order
        self.test_book.remove_order('sell', 52, 't1_4')
        assert len(self.test_book.ask_book_prices) == 0
        assert self.test_book.ask_book[52]['num_orders'] == 0
        assert self.test_book.ask_book[52]['size'] == 0
        assert len(self.test_book.ask_book[52]['order_ids']) == 0
        assert 't1_4' not in self.test_book.ask_book[52]['orders'].keys()
        assert 52 not in self.test_book.ask_book_prices

        #remove 2nd again
        self.test_book.remove_order('sell', 52, 't1_4')
        assert len(self.test_book.ask_book_prices) == 0
        assert self.test_book.ask_book[52]['num_orders'] == 0
        assert self.test_book.ask_book[52]['size'] == 0
        assert len(self.test_book.ask_book[52]['order_ids']) == 0
        assert 't1_4' not in self.test_book.ask_book[52]['orders'].keys()
 
    def test_two(self):
        assert 5 > 1
