from google.appengine.ext import db
from models import Account
import os
import random

def create_world_data():
    from constants import default_counter
    #character data
    character = {}
    character['x'] = 0
    character['y'] = 0
    character['inventory'] = []

    #generate the goal list
    options = range(16)
    goals = 0
    for i in range(8):
        num = random.randint(0, len(options) - 1)
        goals += pow(2,options[num])
        del options[num]

    #attach objects to data set
    data = {}
    data['move_counter'] = default_counter
    data['character'] = character
    data['goals'] = goals
    return data

def template_path(template):
    from constants import template_dir
    path = os.path.join(
        os.path.dirname(__file__) + template_dir, 
        template
    )
    return path

def get_account(user):
    from models import Account
    existing = db.GqlQuery('SELECT * from Account ' +
        'WHERE user = :1',
        user)
    if existing.count() == 0:
        account = Account()
        account.user = user
        account.put()
        return account
    else:
        return existing[0]

def get_active_games(user):
    return db.GqlQuery('SELECT * from Game ' +
                'WHERE players = :1',
            user.nickname())

def is_valid_user(nickname):
    acc = db.GqlQuery('SELECT * from Account ' +
        'WHERE user = USER(:1)',
        nickname + '@gmail.com')
    if acc.count() == 1:
        return True

    return False

def create_new_game(players):
    import uuid
    from models import Game
    game = Game()
    game.game_id = str(uuid.uuid1())
    game.players = players
    game.current_player = random.randint(0, len(players) - 1)
    game.data = create_world_data()
    game.put()
