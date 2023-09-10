import pandas as pd
from sql import *

def engine(phrase):
    phrase = phrase.lower()
    phraseSet = set(phrase)
    cursor.execute("select name from products")
    output = cursor.fetchall()

    matches = []
    
    for name in output:
        nameSet = set(name[0].lower())
        print(phraseSet)
        print(nameSet)
        if len(phraseSet.intersection(nameSet))/len(nameSet) > 0.4:
            matches.append(name[0])
        
    return matches