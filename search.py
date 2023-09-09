import pandas as pd
from sql import cursor

def engine(phrase):
    phrase = phrase.lower()
    cursor.execute("select name from products")
    output = cursor.fetchall()

    matches = []
    
    for name in output:
        matches.append(name[0])
        '''
        if len(set(phrase).intersection(set(name)))/len(set(name))>0.4:
            matches.append(name)
        '''
    return matches

