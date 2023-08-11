# Imported Packages
import pandas as pd
from sql import *

# Welcome Message + Input
account = {}
signin = False
while True:
    dashboard = input('''
Welcome to SathuMart.com! Your one stop shop for every good on the market!

Type 'Search' plus the product you wish to look for to search our catalog.

Type 'Account' to view your Orders, History, and Account Information.

Type 'Sell' to open your Business Dashboard

Type 'Quit' to exit the page.

''')


    match dashboard.lower().split()[0]:

        case 'search':

            query = dashboard.lower().split()[1:]
            print(' '.join(query))

            
            
        case 'account':
            if signin == False:
                while signin == False:
                    try:
                        ID,password = int(input('enter your user id')),input('enter your password')
                        if select_account(ID)['password'] == password:
                            print("You're logged in!")
                            signin = True
                        else:
                            print("Error: password is incorrect")
                            continue

                    except KeyError:
                        print("Your account doesn't exist, please create one")
                        

        case 'sell':
            print('sell')

        case 'quit':
            break

        case _:
            print("Sorry, that command doesn't exist, please try again")
