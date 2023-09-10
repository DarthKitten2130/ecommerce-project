import pandas as pd
from sql import *
from classes import *

def engine(phrase):
    phrase = phrase.lower()
    phraseSet = set(phrase)
    cursor.execute("select * from products")
    output = cursor.fetchall()

    matches = []
    
    for x in output:
        product = Product(
        x[1],
        x[2],
        x[3],
        x[4],
        x[5],
        x[6],
        x[7],)

        df = pd.DataFrame(columns=['name','description','price','discount','discounted price'])

        nameSet = set(product.name.lower())
        if len(phraseSet.intersection(nameSet))/len(nameSet) > 0.4:
            df.loc[x[0]] = [product.name,
                               product.description,
                               product.price,
                               product.discount,
                               product.discounted_price,
                               ]
            matches.append(product.name.lower())
        
    return df