import json

def move_character(game_id, x, y):
    from util import get_game
    #will need a static map of the layout
    game = get_game(game_id)
    data = json.loads(game.data)
    char = data['character']
    diff = abs(int(char['x']) - int(x)) + abs(int(char['y']) - int(y))
    if diff == 1:
        char['x'] = int(x)
        char['y'] = int(y)
        data['character'] = char
        game.data = json.dumps(data)
        game.put()
        return {'x': int(x), 'y': int(y)}
    return False

def do_interaction(game_id, x, y):
    from constants import item_at
    from constants import uses
    from util import get_game
    inter = item_at.get((int(x),int(y)))
    if not inter:
        return False
    
    game = get_game(game_id)
    item = uses.get(inter)
    data = json.loads(game.data)
    status = data['status']
    #It's something we pickup
    if not item:
        status[inter] = 1
        data['status'] = status
        game.data = json.dumps(data)
        game.put()
        return [inter, 1]
    
    #It's something we use something with
    if status[item] == 1:
        status[item] == 2
        data['status'] = status
        game.data = json.dumps(data)
        game.put()
        return [item, 2]
    #We don't have what we need to interact
    else:
        return [inter, 0]
