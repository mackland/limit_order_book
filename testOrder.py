from collections import namedtuple

class Order(namedtuple('Order', 'size side price')):
    def __new__(cls, size, side, price):
        return super(Order, cls).__new__(cls, size, side, price)

test_order = Order(size=200,side='buy',price=49)
print(test_order)
print(test_order.size)
