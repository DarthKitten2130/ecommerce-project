import pandas as pd
from sql import cursor

def engine(phrase):
    
    cursor.execute("select name from products")
    output = cursor.fetchall()
    
    for name in output:
        pass
        
        
engine("Hi")