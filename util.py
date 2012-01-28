from google.appengine.ext import db
from models import Account
import os
import random
import json

def create_world_data():
    from models import Interactions
    #character data
    character = {}
    character['x'] = 0
    character['y'] = 0

    #generate the goal list
    options = range(16)
    goals = 0
    for i in range(8):
        num = random.randint(0, len(options) - 1)
        goals += pow(2,options[num])
        del options[num]

    #attach objects to data set
    data = {}
    data['character'] = character
    data['goals'] = goals
    data['status'] = Interactions().__dict__
 
    return data

def template_path(template):
    from constants import template_dir
    path = os.path.join(
        os.path.dirname(__file__) + template_dir, 
        template
    )
    return path

def get_game(game_id):
    game = db.GqlQuery('SELECT * from Game ' +
        'WHERE game_id = :1',
        game_id)
    if game.count() == 1:
        return game[0]
    return None


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

def get_major_arcana():
    return [
        'fool',
        'magician',
        'priestess',
        'heirophant',
        'hermit',
        'hanged'
        ]

def create_new_game(players):
    import uuid
    from models import Game
    from constants import default_counter
    game = Game()
    game.game_id = str(uuid.uuid1())
    game.players = players
    game.current_player = random.randint(0, len(players) - 1)
    game.data = json.dumps(create_world_data())
    game.move_counter = default_counter
    game.major_arcana = []
    arcana = get_major_arcana()
    for i in range(len(players)):
        num = random.randint(0, len(arcana) - 1)
        game.major_arcana.append(arcana[num])
        del arcana[num]
    game.put()

def validate_player(nickname, game_id):
    if not game_id or game_id == '':
        return False
    game = db.GqlQuery('SELECT * from Game ' +
        'WHERE game_id = :1',
        game_id)
    if game.count() == 1:
        players = game[0].players
        if players[game[0].current_player] == nickname:
            return True
    return False

def get_world_data(nickname, game_id):
    game = get_game(game_id)
    data = json.loads(game.data)
    current = game.current_player
    data['character']['arcana'] = game.major_arcana[current]
    data['move_counter'] = game.move_counter

    return data

