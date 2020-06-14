import pytest
from project.orderbook import Orderbook

@pytest.fixture(scope='function')
def book():
    book = Orderbook()
    
    yield book

@pytest.fixture(scope='function')
def ask_order():
    ask = Orderbook.Order(order_id='s_1', timestamp=1,order_type='add', quantity=200, side='sell', price=49) 
    return ask

@pytest.fixture(scope='function')
def bid_order():
    bid = Orderbook.Order(order_id='b_1', timestamp=1,order_type='add', quantity=200, side='buy', price=49) 
    return bid

def test_add_order_to_history(book, bid_order):
    bid_order.exid = 1
    assert len(book.order_history) == 0
    book.add_order_to_history(bid_order)
    assert bid_order == book.order_history[0]

def test_add_order_to_book_bid(book, bid_order):
    assert len(book.bid_book_prices) == 0
    assert len(book.bid_book) == 0
    book.add_order_to_book(bid_order)
    
    assert len(book.ask_book_prices) == 0
    assert len(book.ask_book) == 0
    assert bid_order.price in book.bid_book_prices
    assert bid_order.price in book.bid_book.keys()
    assert book.bid_book[bid_order.price]['num_orders'] == 1
    assert book.bid_book[bid_order.price]['size'] == bid_order.quantity
    assert book.bid_book[bid_order.price]['order_ids'][0] == bid_order.order_id
 
def test_add_order_to_book_ask(book, ask_order):
    assert len(book.ask_book_prices) == 0
    assert len(book.ask_book) == 0
    book.add_order_to_book(ask_order)
   
    assert len(book.bid_book_prices) == 0
    assert len(book.bid_book) == 0
    assert ask_order.price in book.ask_book_prices
    assert ask_order.price in book.ask_book.keys()
    assert book.ask_book[ask_order.price]['num_orders'] == 1
    assert book.ask_book[ask_order.price]['size'] == ask_order.quantity
    assert book.ask_book[ask_order.price]['order_ids'][0] == ask_order.order_id

def test_remove_order_bid(book):
    b_1 = Orderbook.Order(order_id='b_1', timestamp=1,order_type='add', quantity=200, side='buy', price=49) 
    b_2 = Orderbook.Order(order_id='b_2', timestamp=1,order_type='add', quantity=200, side='buy', price=49) 
    book.add_order_to_book(b_1)
    book.add_order_to_book(b_2)
    
    assert len(book.bid_book[49]['order_ids']) == 2

    #try remove order
    book.remove_order('buy', 49, 'b_1')
    assert book.bid_book[49]['num_orders'] == 1
    assert book.bid_book[49]['size'] == 200
    assert len(book.bid_book[49]['order_ids']) == 1
    assert 'b_1' not in book.bid_book[49]['orders'].keys()
    assert 49 in book.bid_book_prices

    #remove 2nd order
    book.remove_order('buy', 49, 'b_2')
    assert len(book.bid_book_prices) == 0
    assert book.bid_book[49]['num_orders'] == 0
    assert book.bid_book[49]['size'] == 0
    assert len(book.bid_book[49]['order_ids']) == 0
    assert 'b_2' not in book.bid_book[49]['orders'].keys()
    assert 49 not in book.bid_book_prices

    #remove 2nd again
    book.remove_order('buy', 49, 'b_2')
    assert len(book.bid_book_prices) == 0
    assert book.bid_book[49]['num_orders'] == 0
    assert book.bid_book[49]['size'] == 0
    assert len(book.bid_book[49]['order_ids']) == 0
    assert 'b_2' not in book.bid_book[49]['orders'].keys()

def test_remove_order_ask(book):
    s_1 = Orderbook.Order(order_id='s_1', timestamp=1,order_type='add', quantity=200, side='sell', price=52) 
    s_2 = Orderbook.Order(order_id='s_2', timestamp=1,order_type='add', quantity=200, side='sell', price=52) 
    book.add_order_to_book(s_1)
    book.add_order_to_book(s_2)
    
    assert len(book.ask_book[52]['order_ids']) == 2

    #remove sell_order_1
    book.remove_order('sell', 52, 's_1')
    assert book.ask_book[52]['num_orders'] == 1
    assert book.ask_book[52]['size'] == 200
    assert len(book.ask_book[52]['order_ids']) == 1
    assert 's_1' not in book.ask_book[52]['orders'].keys()
    assert 52 in book.ask_book_prices

    #remove 2nd order
    book.remove_order('sell', 52, 's_2')
    assert len(book.ask_book_prices) == 0
    assert book.ask_book[52]['num_orders'] == 0
    assert book.ask_book[52]['size'] == 0
    assert len(book.ask_book[52]['order_ids']) == 0
    assert 's_2' not in book.ask_book[52]['orders'].keys()
    assert 52 not in book.ask_book_prices

    #remove 2nd again
    book.remove_order('sell', 52, 's_2')
    assert len(book.ask_book_prices) == 0
    assert book.ask_book[52]['num_orders'] == 0
    assert book.ask_book[52]['size'] == 0
    assert len(book.ask_book[52]['order_ids']) == 0
    assert 's_2' not in book.ask_book[52]['orders'].keys()

def test_modify_order_bid(book, bid_order):
    '''Add orders, remove partial then the remaining''' 
    book.add_order_to_book(bid_order)
    
    book.modify_order('buy', 100, 'b_1', 49)
    assert book.bid_book[49]['size'] == 100
    assert book.bid_book[49]['orders']['b_1'].quantity == 100
    assert 49 in book.bid_book_prices

    book.modify_order('buy', 100, 'b_1', 49)
    assert len(book.bid_book_prices) == 0
    assert book.bid_book[49]['num_orders'] == 0
    assert book.bid_book[49]['size'] == 0
    assert 49 not in book.bid_book_prices
    assert 'b_1' not in book.bid_book[49]['orders'].keys()

def test_modify_order_ask(book, ask_order):
    book.add_order_to_book(ask_order)

    book.modify_order('sell', 100, 's_1', 49)
    assert book.ask_book[49]['size'] == 100
    assert book.ask_book[49]['orders']['s_1'].quantity == 100
    assert 49 in book.ask_book_prices

    book.modify_order('sell', 100, 's_1', 49)
    assert len(book.ask_book_prices) == 0
    assert book.ask_book[49]['num_orders'] == 0
    assert book.ask_book[49]['size'] == 0
    assert 's_1' not in book.ask_book[49]['orders'].keys()
