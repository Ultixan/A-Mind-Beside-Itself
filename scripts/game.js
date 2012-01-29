var x_offset = 150;
var y_offset = 400;

var data;

function getParams() {
    var cleanString = location.search.slice(1);
    var paramArray = cleanString.split('&');
    var params = {};
    $.each(paramArray, function(index, param) {
        var parts = param.split('=');
        params[parts[0]] = parts[1];
    });
    return params;
}

function getPos(xin, yin) {
    a = xin + yin - 1;
    b = (2 * yin) - a;
    xpos = (a * 32) + x_offset;
    ypos = (b * 16) + y_offset;
    return {x: xpos, y: ypos}
}

function buildPlatform() {
    for (var x=0; x < 20; x+=1) {
        for (var y=0; y <11; y+=1) {
            var pos = getPos(x, y);
            var img = $('<img/>');
            img.attr('src', 'images/concrete1.png');
            img.css('position', 'absolute');
            img.css('right', pos.x + 'px');
            img.css('bottom', pos.y + 'px');
            $('body').append(img);
        }
    }
}

var handlePopulate = function(response) {
    data = JSON.parse(response);
    var pos = getPos(
            data['character']['x'],
            data['character']['y']);
    var player = $('<img id="player"/>');
    player.attr('src', 'images/wisp.png');
    player.css('position', 'absolute');
    player.css('right', pos.x + 'px');
    player.css('bottom', pos.y + 'px');
    var arrow = 
    $('body').append(player);
};

function getGameData() {
    var params = getParams();
    $.post('populate', {
        'game_id': params['game_id']
    },
    handlePopulate);
}

var startup = function() {
    buildPlatform();
    getGameData();
};

$(document).ready(startup);

var moveWisp = function(x, y) {
    
}
