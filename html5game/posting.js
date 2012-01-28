function getParams() {
    var cleanString = location.search.slice(1);
    var paramArray = cleanString.split('&');
    var params = {};
    $.each(paramArray, function(index, item) {
         var parts = item.split('=');
         params[parts[0]] = parts[1];
    });
    return params;
}

function validity_check(response) {
    console.log(response);
}

function position_post(gridX, gridY) {
    var params = getParams();
    $.post('move', {
        game_id: params['game_id'],
        x: gridX, 
        y: gridY
    }, 
    validity_check);
}

function getCharacterPosition() {
    if (!Data) {
        return null;
    }

    var wisp = Data['character'];
    return [wisp['x'], wisp['y']]; 
}

function getGoalData() {
    if (!Data) {
        return null;
    }

    var goals = Data['character']['goals'];
    var stats = Data['status'];
    
    return {
        goals[0]: (stats[goals[0]] == 2),
        goals[1]: (stats[goals[1] == 2)
    };
}
