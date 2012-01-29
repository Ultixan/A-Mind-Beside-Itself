from google.appengine.ext import db
from models import Account
import os
import random
import json

def create_world_data():
    from models import Interactions
    #character data
    character = {}
    character['x'] = 9
    character['y'] = 5

    #attach objects to data set
    data = {}
    data['character'] = character
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

def get_goals():
    return {
        'sword': ['chair','doll','matchbox','knife'],
        'coin': ['silver','purse','gold','card'],
        'cup': ['bottle','food','milk','bread'],
        'wand': ['cloth','ticket','pen','key']
        }

def create_new_game(players, name):
    import uuid
    from models import Game
    from constants import default_counter
    from constants import win_types
    game = Game()
    game.game_name = name
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
    
    goals = get_goals()
    game.goals = []
    for i in game.major_arcana:
        for goal in win_types[i]:
            num = random.randint(0, len(goals[goal]) - 1)
            game.goals.append(goals[goal][num])
            del goals[goal][num]

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
    data['character']['goals'] = []
    data['character']['goals'].append(game.goals[current * 2])
    data['character']['goals'].append(game.goals[(current * 2) + 1])

    return data

