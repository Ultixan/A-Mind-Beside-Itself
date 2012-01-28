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
