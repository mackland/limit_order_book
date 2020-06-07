from project.orderbook import Orderbook

test_book = Orderbook()
buy_order_1 = {'order_id': 't1_1', 'timestamp': 2, 'type': 'add', 'quantity': 1, 'side': 'buy', 'price': 50}
buy_order_2 = {'order_id': 't1_2', 'timestamp': 3, 'type': 'add', 'quantity': 1, 'side': 'buy', 'price': 50}
buy_order_3 = {'order_id': 't10_1', 'timestamp': 4, 'type': 'add', 'quantity': 3, 'side': 'buy', 'price': 49}
buy_order_4 = {'order_id': 't11_1', 'timestamp': 5, 'type': 'add', 'quantity': 3, 'side': 'buy', 'price': 47}
sell_order_1 = {'order_id': 't1_3', 'timestamp': 2, 'type': 'add', 'quantity': 1, 'side': 'sell', 'price': 52}
sell_order_2 = {'order_id': 't1_4', 'timestamp': 3, 'type': 'add', 'quantity': 1, 'side': 'sell', 'price': 52}
sell_order_3 = {'order_id': 't10_2', 'timestamp': 4, 'type': 'add', 'quantity': 3, 'side': 'sell', 'price': 53}
sell_order_4 = {'order_id': 't11_2', 'timestamp': 5, 'type': 'add', 'quantity': 3, 'side': 'sell', 'price': 55}

def test_add_order_to_history():
    '''test add_order_to_history()'''
    test_order = {'order_id': 't1_5', 'timestamp': 4, 'type': 'add', 'quantity': 5, 'side': 'sell', 'price': 55}
    assert len(test_book.order_history) == 0
    test_order['exid'] = 1
    test_book.add_order_to_history(test_order)
    assert test_order == test_book.order_history[0]

def test_add_order_to_book():
    '''Add two buy orders, 2 sell to check bid/ask_book and bid/ask_book_prices'''
    assert len(test_book.bid_book_prices) == 0
    assert len(test_book.bid_book) == 0
    
    test_book.add_order_to_book(buy_order_1)
    assert 50 in test_book.bid_book_prices
    assert 50 in test_book.bid_book.keys()
    assert test_book.bid_book[50]['num_orders'] == 1
    assert test_book.bid_book[50]['size'] == 1
    assert test_book.bid_book[50]['order_ids'][0] == buy_order_1['order_id']
    
    test_book.add_order_to_book(buy_order_2)
    assert test_book.bid_book[50]['num_orders'] == 2
    assert test_book.bid_book[50]['size'] == 2
    assert test_book.bid_book[50]['order_ids'][1] == buy_order_2['order_id']
    assert test_book.bid_book[50]['orders'][buy_order_2['order_id']] == buy_order_2
 
    assert len(test_book.ask_book_prices) == 0
    assert len(test_book.ask_book) == 0

    test_book.add_order_to_book(sell_order_1)
    assert 52 in test_book.ask_book_prices
    assert 52 in test_book.ask_book.keys()
    assert test_book.ask_book[52]['num_orders'] == 1
    assert test_book.ask_book[52]['size'] == 1
    assert test_book.ask_book[52]['order_ids'][0] == sell_order_1['order_id']

    test_book.add_order_to_book(sell_order_2)
    assert test_book.ask_book[52]['num_orders'] == 2
    assert test_book.ask_book[52]['size'] == 2
    assert test_book.ask_book[52]['order_ids'][1] == sell_order_2['order_id']
    assert test_book.ask_book[52]['orders'][sell_order_2['order_id']] == sell_order_2

def test_two():
    assert 5 > 1
