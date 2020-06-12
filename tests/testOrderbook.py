import pytest
from project.orderbook import Orderbook

@pytest.fixture(scope='function')
def book():
    book = Orderbook()
    
    yield book

def test_add_order_to_history(book):
    test_order = {'order_id':'test','timestamp':1,'type':'add','quantity':50,'side':'sell','price':140,'exid':1}
    assert len(book.order_history) == 0
    book.add_order_to_history(test_order)
    assert test_order == book.order_history[0]

@pytest.mark.parametrize(
        'order_id,timestamp,types,quantity,side,price', 
        [
            ('t1_1','1','add',1,'buy',50),
            ('t1_2','2','add',2,'buy',49),
            ('t1_3','3','add',4,'sell',48),
            ('t1_4','4','add',5,'sell',47),
            ('t1_5','5','add',120,'buy',45), 
            ('t1_6','6','add',500,'buy',127), 
            ('t1_7','7','add',250,'sell',299), 
            ]
        )
def test_add_order_to_book(book,order_id,timestamp,types,quantity,side,price):
    assert len(book.bid_book_prices) == 0
    assert len(book.ask_book_prices) == 0
    assert len(book.bid_book) == 0
    assert len(book.ask_book) == 0

    test_order = {'order_id':order_id,'timestamp':timestamp,'type':types,'quantity':quantity,'side':side,'price':price} 
    book.add_order_to_book(test_order)
    
    if side == 'buy':
        assert price in book.bid_book_prices
        assert price in book.bid_book.keys()
        assert book.bid_book[price]['num_orders'] == 1
        assert book.bid_book[price]['size'] == quantity
        assert book.bid_book[price]['order_ids'][0] == order_id
    else:
        assert price in book.ask_book_prices
        assert price in book.ask_book.keys()
        assert book.ask_book[price]['num_orders'] == 1
        assert book.ask_book[price]['size'] == quantity
        assert book.ask_book[price]['order_ids'][0] == order_id

#def test_remove_order(self):
#    self.test_book.add_order_to_book(self.buy_order_1)
#    self.test_book.add_order_to_book(self.buy_order_2)
#    assert 50 in self.test_book.bid_book_prices
#    assert 50 in self.test_book.bid_book.keys()
#    assert self.test_book.bid_book[50]['num_orders'] == 2
#    assert self.test_book.bid_book[50]['size'] == 2
#    assert len(self.test_book.bid_book[50]['order_ids']) == 2
#
#    #try remove order
#    self.test_book.remove_order('buy', 50, 't1_1')
#    assert self.test_book.bid_book[50]['num_orders'] == 1
#    assert self.test_book.bid_book[50]['size'] == 1
#    assert len(self.test_book.bid_book) == 1
#    assert 't1_1' not in self.test_book.bid_book[50]['orders'].keys()
#    assert 50 in self.test_book.bid_book_prices
#
#    #remove 2nd order
#    self.test_book.remove_order('buy', 50, 't1_2')
#    assert len(self.test_book.bid_book_prices) == 0
#    assert self.test_book.bid_book[50]['num_orders'] == 0
#    assert self.test_book.bid_book[50]['size'] == 0
#    assert len(self.test_book.bid_book[50]['order_ids']) == 0
#    assert 't1_2' not in self.test_book.bid_book[50]['orders'].keys()
#    assert 50 not in self.test_book.bid_book_prices
#
#    #remove 2nd again
#    self.test_book.remove_order('buy', 50, 't1_2')
#    assert len(self.test_book.bid_book_prices) == 0
#    assert self.test_book.bid_book[50]['num_orders'] == 0
#    assert self.test_book.bid_book[50]['size'] == 0
#    assert len(self.test_book.bid_book[50]['order_ids']) == 0
#    assert 't1_2' not in self.test_book.bid_book[50]['orders'].keys()
#    
#    #test for ask book
#    self.test_book.add_order_to_book(self.sell_order_1)
#    self.test_book.add_order_to_book(self.sell_order_2)
#    assert 52 in self.test_book.ask_book_prices
#    assert 52 in self.test_book.ask_book.keys()
#    assert self.test_book.ask_book[52]['num_orders'] == 2
#    assert self.test_book.ask_book[52]['size'] == 2
#    assert len(self.test_book.ask_book[52]['order_ids']) == 2
#
#    #remove sell_order_1
#    self.test_book.remove_order('sell', 52, 't1_3')
#    assert self.test_book.ask_book[52]['num_orders'] == 1
#    assert self.test_book.ask_book[52]['size'] == 1
#    assert len(self.test_book.ask_book[52]['order_ids']) == 1
#    assert 't1_3' not in self.test_book.ask_book[52]['orders'].keys()
#    assert 52 in self.test_book.ask_book_prices
#
#    #remove 2nd order
#    self.test_book.remove_order('sell', 52, 't1_4')
#    assert len(self.test_book.ask_book_prices) == 0
#    assert self.test_book.ask_book[52]['num_orders'] == 0
#    assert self.test_book.ask_book[52]['size'] == 0
#    assert len(self.test_book.ask_book[52]['order_ids']) == 0
#    assert 't1_4' not in self.test_book.ask_book[52]['orders'].keys()
#    assert 52 not in self.test_book.ask_book_prices
#
#    #remove 2nd again
#    self.test_book.remove_order('sell', 52, 't1_4')
#    assert len(self.test_book.ask_book_prices) == 0
#    assert self.test_book.ask_book[52]['num_orders'] == 0
#    assert self.test_book.ask_book[52]['size'] == 0
#    assert len(self.test_book.ask_book[52]['order_ids']) == 0
#    assert 't1_4' not in self.test_book.ask_book[52]['orders'].keys()
#
#def test_modify_order(self):
#    ''Add orders, remove partial then the remaining''
#    
#    # Test bid book
#    self.test_book.add_order_to_book(self.buy_order_3)
#    assert self.test_book.bid_book[49]['size'] == 3
#    
#    self.test_book.modify_order('buy', 2, 't10_1', 49)
#    assert self.test_book.bid_book[49]['size'] == 1
#    assert self.test_book.bid_book[49]['orders']['t10_1']['quantity'] == 1
#    assert 49 in self.test_book.bid_book_prices
#
#    self.test_book.modify_order('buy', 1, 't10_1', 49)
#    assert len(self.test_book.bid_book_prices) == 0
#    assert self.test_book.bid_book[49]['num_orders'] == 0
#    assert self.test_book.bid_book[49]['size'] == 0
#    assert 49 not in self.test_book.bid_book_prices
#    assert 't10_1' not in self.test_book.bid_book[49]['orders'].keys()
#
#    # Test the ask book
#    self.test_book.add_order_to_book(self.sell_order_3)
#    assert self.test_book.ask_book[53]['size'] == 3
#
#    self.test_book.modify_order('sell', 2, 't10_2', 53)
#    assert self.test_book.ask_book[53]['size'] == 1
#    assert self.test_book.ask_book[53]['orders']['t10_2']['quantity'] == 1
#    assert 53 in self.test_book.ask_book_prices
#
#    self.test_book.modify_order('sell', 1, 't10_2', 53)
#    assert len(self.test_book.ask_book_prices) == 0
#    assert self.test_book.ask_book[53]['num_orders'] == 0
#    assert self.test_book.ask_book[53]['size'] == 0
#    assert 't10_2' not in self.test_book.ask_book[53]['orders'].keys()
#
#def test_two(self):
#    assert 5 > 1
#
