import json

def move_character(game_id, x, y):
    from util import get_game
    from constants import item_at
    from constants import default_counter
    #will need a static map of the layout
    if int(x) > 19 or int(y) > 10 or int(x) < 0 or int(y) < 0:
        return False
    game = get_game(game_id)
    data = json.loads(game.data)
    char = data['character']
    diff = abs(int(char['x']) - int(x)) + abs(int(char['y']) - int(y))
    if diff == 1:
        item = item_at.get((int(x), int(y)))
        if item and (not item in data['status'] or data['status'][item] == 0):
            return False
        char['x'] = int(x)
        char['y'] = int(y)
        data['character'] = char
        game.data = json.dumps(data)
        game.move_counter = game.move_counter - 1
        if game.move_counter == 0:
            game.current_player = game.current_player + 1
            game.move_counter = default_counter
            if game.current_player == len(game.players):
                game.current_player = 0
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
        
        for index in range(0,len(game.players)):
            goal1_status = data['status'][game.goals[2*index]
            goal2_status = data['status'][game.goals[2*index+1]
            if (goal1_status + goal2_status == 4 ):
                if(index == game.current_player):
                    return ["winner", game.players[index]]
                else:
                    return ["loser", game.players[index]]
   
        return [item, 2]
    #We don't have what we need to interact
    else:
        return [inter, 0]
