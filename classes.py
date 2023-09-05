from sql import *
from statistics import mean

class Product:
    
    def __init__(self,category,name,description,price,discount,stock):
        self.category = category
        self.name = name
        self.description = description
        self.price = price
        self.discount = discount
        self.discounted_price = self.price * self.discount
        self.stock = stock
        self.reviews = []
        self.avgrating = mean(self.reviews)
    
    def has_stock(self):
        return lambda stock: True if self.stock > 0 else False
    
    def insert_review(self,user,rating,review):
        self.reviews.append({'user': user,
                             'rating': rating,
                             'review': review})
    
    
    
    
    
    
    
    