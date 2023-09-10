from statistics import mean

class Product:
    
    def __init__(self,name,description,price,discount,stock,category,seller):
        
        self.name = name
        self.description = description
        self.price = price
        self.discount = discount
        self.discounted_price = self.price * self.discount
        self.stock = stock
        self.category = category
        self.seller = seller
        self.reviews = []
    
    def has_stock(self):
        return lambda stock: True if self.stock > 0 else False
    
    def insert_review(self,user,rating,review):
        self.reviews.append({'user': user,
                             'rating': rating,
                             'review': review})
    
    
    
    
    
    
    
    