from sql import *

class Product:
    
    def __init__(self,name,description,price,discount,stock):
        self.name = name
        self.description = description
        self.price = price
        self.discount = discount
        self.discounted_price = self.price * self.discount
    
    
    def has_stock(self,stock):
        return lambda stock: True if stock > 0 else False
    
    
    
    