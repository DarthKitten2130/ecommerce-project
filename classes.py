class Product:
    
    def __init__(self,id,name,description,price,discount,stock,category,seller):
        
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.discount = discount
        self.discounted_price = self.price * (1-self.discount)
        self.stock = stock
        self.category = category
        self.seller = seller
    
    
    
    
    
    
    
    