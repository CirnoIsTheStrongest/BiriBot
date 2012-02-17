from random import randint as random
import json
from ModuleBase import *

class Railgun(object):
    ''' module for the .railgun counting game '''

    def __init__(self, user):
        self.user = user
        self.railgun_db = 'railguns.json'
        self.user_db = 'railgun_users.json'

    def register_user(self, source_):
        registration = register_user_(source_, self.user, self.user_db)

    def railguns(self):
        railguns = random(1,120)
        if railguns in range(1,5):
            railguns = 0
        elif railguns in range(5,40):
            railguns = 1
        elif railguns in range(40,60):
            railguns = 2
        elif railguns in range(60,80):
            railguns = 3
        elif railguns in range(80,100):
            railguns = 4
        elif railguns in range(100,115):
            railguns = 5
        elif railguns in range(115,121):
            railguns = 6
        return railguns

    
    def last_orders(self):
        last_orders = random(1,50)
        if last_orders in range(1,5):
            last_orders = 0
        elif last_orders in range(5,35):
            last_orders = 1
        elif last_orders in range(35,45):
            last_orders = 2
        elif last_orders in range(45,51):
            last_orders = 3
        return last_orders

    def misakas(self):
        misakas = random(1,120)
        if misakas in range(1,5):
            misakas = 0
        elif misakas in range(5,40):
            misakas = random(1,3)
        elif misakas in range(40,70):
            misakas = random(3,6)
        elif misakas in range(70, 100):
            misakas = random(6,9)
        elif misakas in range(100,115):
            misakas = random(9,12)
        elif misakas in range(115,121):
            misakas = 12
        return misakas

    def give_or_take(self):
        choice = random(1,100)
        if choice in range(1,71):
            positive = True
        else:
            positive = False
        return positive

    def get_prizes(self):
        ''' function for generating the random number of railguns and weights'''
        user = check_alias(self.user, self.user_db)
        misakas = self.misakas()
        last_orders = self.last_orders()
        railguns = self.railguns()
        receipt_choice = self.give_or_take()
        if receipt_choice == True:
            receipt = 'You received: '
        else:
            receipt = 'You lost: '
        try:
            prize_dict = open_user_database(self.railgun_db)
        except IOError:
            prize_dict = {}
            prize_dict[user] = {'misakas':misakas, 'railguns':railguns, 'last_orders':last_orders}
            save_user_database(prize_dict, self.railgun_db)
            return '{0} {1} MISAKAS, {2} Railguns, {3} Last Orders.'.format(receipt,misakas, railguns, last_orders)

        total_misakas = prize_dict[user]['misakas']
        total_last_orders = prize_dict[user]['last_orders']
        total_railguns = prize_dict[user]['railguns']

        if receipt_choice == True:
            prize_dict[user]['misakas'] += misakas
            prize_dict[user]['railguns'] += railguns
            prize_dict[user]['last_orders'] += last_orders
            save_user_database(prize_dict, self.railgun_db)
        
        else:
            prize_dict[user]['misakas'] -= misakas
            prize_dict[user]['railguns'] -= railguns
            prize_dict[user]['last_orders'] -= last_orders
            save_user_database(prize_dict, self.railgun_db)

        return '{0} {1} MISAKAS, {2} Railguns, {3} Last Orders.'.format(receipt, misakas, railguns, last_orders)

    def check_stats(self):
        ''' function for checking your current score '''
        user = check_alias(self.user, self.user_db)
        