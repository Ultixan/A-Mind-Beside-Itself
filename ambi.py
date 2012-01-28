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
        return True
    return False
