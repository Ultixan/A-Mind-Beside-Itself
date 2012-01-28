from google.appengine.ext import db

class Game(db.Model):
    game_id = db.StringProperty()
    players = db.StringListProperty()
    current_player = db.IntegerProperty()
    goals = db.IntegerProperty()
    content = db.ListProperty(int)
    move_counter = db.IntegerProperty()

class Player(db.Model):
    game_id = db.StringProperty()
    x = db.IntegerProperty()
    y = db.IntegerProperty()

class Account(db.Model):
    user = db.UserProperty()
    games = db.StringListProperty()
