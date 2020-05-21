#TODO:
# process order function
# make util function to get book, prices 
class Orderbook():
    def __init__(self):
        self.order_history = []
        self.bid_book = {}
        self.bid_book_prices = []
        self.ask_book = {}
        self.ask_book_prices = []
        self.confirm_modify_collector = []
        self.confirm_trade_collector = []
        self.trade_book = []
        self.order_index = 0
        self.traded = False

    def add_order_to_history(self, order):
       '''Add order to order_history'''
        hist_order = {
                'order_id': order['order_id'],
                'timestamp': order['timestamp'],
                'type': order['type'],
                'quantity': order['quantity'],
                'side' = order['side']
                'price' = order['price']
                }
        self.order_index += 1
        historder['exid'] = self.order_index
        self.order_history.append(hist_order)
        
    def add_order_to_book(self, order):
        '''Use insort to maintain ordered list of prices, which are pointers to orders'''
        book_order = {
                'order_id': order['order_id'],
                'timestamp': order['timestamp'],
                'type': order['type'],
                'quantity': order['quantity'],
                'side': order['side'],
                'price': order['price']
                }
        if order['side'] == 'buy':
            book_prices = self.bid_book_prices
            book = self.bid_book
        else:
            book_prices = self.ask_book_prices
            book = self.ask_book
        if order['price'] in book_prices:
            book[order['price']]['num_orders'] += 1
            book[order['price']]['size'] += order['quantity']
            book[order['price']]['order_ids'].append(order['order_id'])
            book[order['price']]['orders'][order['order_id']] = book_order
        else:
            bisect.insort(book_prices, order['price'])
            book[order['price']] = {
                    'num_orders': 1,
                    'size': order['quantity'],
                    'order_ids': [order['order_id']],
                    'orders': {order['order_id']: book_order}
                    }

    def remove_order(self, order_side, order_price, order_id):
        '''If order exists, remove from book'''
        if order_side == 'buy':
            book_prices = self.bid_book_prices
            book = self.bid_book
        else: # order_side == 'sell'
            book_prices = self.ask_book_prices
            book = self.ask_book

        is_order = book[order_price]['orders'].pop(order_id, None)
        if is_order:
            book[order_price]['num_orders'] -= 1
            book[order_price]['size'] -= is_order['quantity']
            book[order_price]['order_ids'].remove(is_order['order_id'])
            if book[order_price]['num_orders'] == 0:
                book_prices.remove(order_price)

    def modify_order(self, order_size, order_quantity, order_id, order_price):
        '''If order_quantity = 0, remove order'''
        book = self.bid_book if order_side == 'buy' else self.ask_book

        if order_quantity < book[order_price]['orders'][order_id]['quantity']:
            book[order_price]['size'] -= order_quantity
            book[order_price]['orders'][order_id]['quantity'] -= order_quantity
        else:
            self.remove_order(order_size, order_price, order_id)


    def add_trade_to_book(self, resting_order_id, resting_timestamp, incoming_order_id, timestamp, price, quantity, side):
        '''Add trade to the trade_book list.'''
        self.trade_book.append(
                {
                    'resting_order_id': resting_order_id,
                    'resting_timestamp': resting_timestamp,
                    'incoming_order_id': incoming_order_id,
                    'timestamp': timestamp,
                    'price': price,
                    'quantity': quantity,
                    'side': side
                    }
                )
    def confirm_trade(self, timestamp, order_side, order_quantity, order_id, order_price):

    def confirm_modify(self, timestamp, order_side, order_quantity, order_id):

    def process_order(self, order): #this will do most of the work
        '''Check if match with ersting order, if so call match_trade. Else update the book'''
        self.confirm_modify_collector.clear()
        self.traded = False
        self.add_order_to_history(order)

        if order['type'] == 'add':
            if order['side'] == 'buy':
                if order['price'] >= self.ask_book_prices[0]:
                    self.match_trade(order)
                else:
                    self.add_order_to_book(order)
            else: #order = sell
                if order['price'] <= self.bid_book_prices[-1]:
                    self.match_trade(order)
                else:
                    self.add_order_to_book(order)
        else:
            if order['side'] == 'buy':
                book = self.bid_book
                book_prices = self.bid_book_prices
            else:
                book = self.ask_book
                book_prices = self.ask_book_prices
            if order['price'] in book_prices:
                if order['order_id' in book[order['price']]['orders']:
                    self.confirm_modify(order['timestamp'], order['side'], order['quantity'], order['order_id'])
                    if order['type'] == 'cancel':
                        self.remove_order(order['side'], order['price'], order['order_id'])
                    else: #type == modify
                        self.modify_order(order['side'], order['quantity'], order['order_id'], order['price'])

    def match_trade(self, order):
        ''' 
        Match order with resting orders on the book, once matched will remove resting order or modify by number of shares of the incoming order
        '''
        self.traded = True
         
        if order['side'] == 'buy':
            book_prices = self.ask_book_prices
            book = self.ask_book
            remainder = order['quantity']

            while remainder > 0:
                if book_prices:
                    price = book_prices[0]
                    if order['price'] >= price: 
                        book_order_id = book[price]['order_ids'][0]
                        book_order = book[price]['orders'][book_order_id]
                        if remainder >= book_order['quantity']: #if buy order larger than order on the book, execute at that price and remove the resting order
                            self.confirm_trade(order['timestamp'], book_order['side'], book_order['quantity'], 
                                    book_order['order_id'], book_order['price'])
                            self.add_trade_to_book(book_order['order_id'], book_order['timestamp'], order['order_id'], 
                                    order['timestamp'], book_order['price'], book_order['quantity'], order['side'])
                            self.remove_order(book_order['side'], book_order['price'], book_order['order_id'])
                            remainder -= book_order['quantity']
                        else: # trade will take place but will only reduce the resting order quantity by # of shares
                            self.confirm_trade(order['timestamp'], book_order['side'], remainder, 
                                    book_order['order_id'], book_order['price'])
                            self.add_trade_to_book(book_order['order_id'], book_order['timestamp'], order['order_id'], 
                                    order['timestamp'], book_order['price'], remainder, order['side'])
                            self.modify_order(book_order['side'], remainder, book_order['order_id'], book_order['price'])
                            break
                    else: #no immediate match, add order to book
                        order['quantity'] = remainder
                        self.add_order_to_book(order)
                        break
                else:
                    print('No orders on book after order {0}'.format(order))
                    break
        else: #order['side'] == 'sell'
            book_prices = self.bid_book_prices
            book = self.bid_book
            remainder = order['quantity']
            while remainder > 0:
                if book_prices:
                    price = book_prices[-1]
                    if order['price'] <= price:
                        book_order_id = book[price]['order_ids'][0]
                        book_order = book[price]['orders'][book_order_id]
                        if remainder >= book_order['quantity']:
                            self.confirm_trade(order['timestamp'], book_order['side'], book_order['quantity'], 
                                    book_order['order_id'], book_order['price'])
                            self.add_trade_to_book(book_order['order_id'], book_order['timestamp'], order['order_id'], 
                                    order['timestamp'], book_order['price'], book_order['quantity'], order['side'])
                            self.remove_order(book_order['side'], book_order['price'], book_order['order_id'])
                            remainder -= book_order['quantity']
                        else: # trade will take place but will only reduce the resting order quantity by # of shares
                            self.confirm_trade(order['timestamp'], book_order['side'], remainder, book_order['order_id'], book_order['price'])
                            self.add_trade_to_book(book_order['order_id'], book_order['timestamp'], order['order_id'], 
                                    order['timestamp'], book_order['price'], remainder, order['side'])
                            self.modify_order(book_order['side'], remainder, book_order['order_id'], book_order['price'])
                            break
 
                    else:
                        order['quantity'] = remainder
                        self.add_order_to_book(order)
                        break
                else:
                    print('No orders on bid book with order {0}'.format(order))
                    break

