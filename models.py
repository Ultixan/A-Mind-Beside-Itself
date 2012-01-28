from google.appengine.ext import db

class Game(db.Model):
    game_id = db.StringProperty()
    game_name = db.StringProperty()
    players = db.StringListProperty()
    current_player = db.IntegerProperty()
    major_arcana = db.StringListProperty()
    goals = db.IntegerProperty()
    move_counter = db.IntegerProperty()
    data = db.TextProperty()

class Player(db.Model):
    game_id = db.StringProperty()
    x = db.IntegerProperty()
    y = db.IntegerProperty()

class Account(db.Model):
    user = db.UserProperty()
    win = db.IntegerProperty()
    lose = db.IntegerProperty()

class Interactions:
    #set up object statuses
    def __init__(self):
        #sword
        self.chair = 0
        self.doll = 0
        self.matchbox = 0
        self.knife = 0

        #coin
        self.silver = 0
        self.purse = 0
        self.gold = 0
        self.card = 0

        #cup
        self.bottle = 0
        self.food = 0
        self.milk = 0
        self.bread = 0

        #wand
        self.cloth = 0
        self.ticket = 0
        self.pen = 0
        self.key = 0
