var x_offset = 100;
var y_offset = 400;

var data;

var titles = {
    'chair': 'Bring the chair to the old lady',
    'doll': 'Bring the doll to the girl',
    'matchbox': 'Use match to light lantern',
    'knife': 'Use knife to scare villain',
    'silver': 'Use silver coin to make a phone call',
    'purse': 'Return purse to woman',
    'gold': 'Use gold coin at ticket booth',
    'card': 'Use credit card on ATM',
    'bottle': 'Fill the bottle with water',
    'food': 'Give food to the homeless man',
    'milk': 'Give milk to the cat',
    'bread': 'Give bread to the bird',
    'cloth': 'Use cloth to clean mirror',
    'ticket': 'Return the ticket to the man',
    'pen': 'Use the pen to change the signpost',
    'key': 'Use the key to change the clock'
}

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

var moveWisp = function(response, dummy) {
    if (!response || response === 'false') {
        return;
    }
    if (!response.x) {
        response = JSON.parse(response);
    }
    data['character']['x'] = response['x'];
    data['character']['y'] = response['y'];
    var pos = getPos(response['x'], response['y']);
    var player = $('#player');
    player.css('right', pos.x + 'px');
    player.css('bottom', pos.y + 'px');
    player.trigger('moved');
    
    if (dummy === 'success') {
        data['move_counter'] -= 1;
        if (data['move_counter'] == 0) {
            window.location.reload();
        } else {
            $('#counter>span').text(data['move_counter']);
        }
    }
};

var tryMove = function(x, y) {
    var params = getParams();
    $.post('move', {
        'game_id': params['game_id'],
        'x': x,
        'y': y
    },
    moveWisp);
};

var item_map = [];

var loadInteractions = function(response) {
    var items = JSON.parse(response);
    var body = $('body');
    for (var item in items) {
        if (!data['status'][item]) {
            var elem = $('<img/>');
            elem.attr('id', item);
            elem.attr('title', item);
            elem.attr('src', 'images/' + item + '.png');
            elem.css('position', 'absolute');
            var pos = getPos(items[item][0], items[item][1]);
            item_map.push(pos);
            elem.css('right', pos.x);
            elem.css('bottom', pos.y);
            body.append(elem);
        }
    }
}

var handleInteraction = function(response) {
    if (response === 'false') {
        return;
    }
    var item = JSON.parse(response);
    if (item[1] === 1) {
        $('#' + item[0]).remove();
    }    
};

function interact(x, y) {
    var params = getParams();
    $.post('interact', {
        'game_id': params['game_id'],
        'x': x,
        'y': y
    },
    handleInteraction);
}

var handlePopulate = function(response) {
    data = JSON.parse(response);
    $('#counter>span').text(data['move_counter']);
    var card = $('#major_arcana');
    card.attr('src', 'images/cards/major/' +
            data['character']['arcana'] +
            '.png');
    card.css('display', 'block');
    var minor1 = $('#minor1');
    minor1.attr('src', 'images/cards/' +
            data['character']['goals'][0] +
            '.png');
    minor1.css('display', 'block');
    minor1.attr('title', titles[data['character']['goals'][0]]);
    var minor2 = $('#minor2');
    minor2.attr('src', 'images/cards/' +
            data['character']['goals'][1] +
            '.png');
    minor2.css('display', 'block');
    minor2.attr('title', titles[data['character']['goals'][1]]);
    var pos = getPos(
            data['character']['x'],
            data['character']['y']);
    var player = $('<img id="player"/>');
    player.attr('src', 'images/wisp.png');
    player.css('position', 'absolute');
    player.css('right', pos.x + 'px');
    player.css('bottom', pos.y + 'px');
    player.css('z-index', '5');
    var tr = $('<img class="arrow" id="tr"/>');
    tr.attr('src', 'images/arrow_tr.png');
    tr.bind('click', function() {
        if (tr.attr('src') === 'images/arrow_tr.png') {
            tryMove(
                data['character']['x'] - 1,
                data['character']['y']
            );
        } else {
            interact(
                data['character']['x'] - 1,
                data['character']['y']
            );
        }
    });
    var tl = $('<img class="arrow" id="tl"/>');
    tl.attr('src', 'images/arrow_tl.png');
    tl.bind('click', function() {
        if (tl.attr('src') === 'images/arrow_tl.png') {
            tryMove(
                data['character']['x'],
                data['character']['y'] + 1
            );
        } else {
            interact(
                data['character']['x'],
                data['character']['y'] + 1
            );
        }
    });
    var br = $('<img class="arrow" id="br"/>');
    br.attr('src', 'images/arrow_br.png');
    br.bind('click', function() {
        if (br.attr('src') === 'images/arrow_br.png') {
            tryMove(
                data['character']['x'],
                data['character']['y'] - 1
            );
        } else {
            interact(
                data['character']['x'],
                data['character']['y'] - 1
            );
        }
    });
    var bl = $('<img class="arrow" id="bl"/>');
    bl.attr('src', 'images/arrow_bl.png');
    bl.bind('click', function() {
        if (bl.attr('src') === 'images/arrow_bl.png') {
            tryMove(
                data['character']['x'] + 1,
                data['character']['y']
            );
        } else {
            interact(
                data['character']['x'] + 1,
                data['character']['y']
            );
        }
    });
    
    player.bind('moved', function() {
        var x = data['character']['x'];
        var y = data['character']['y'];
        var pos_tr = getPos(x-1,y);
        var pos_tl = getPos(x,y+1);
        var pos_br = getPos(x,y-1);
        var pos_bl = getPos(x+1,y);
        var hit = function(pos) {
            var match = false;
            $.each(item_map, function(index, item) {
                if (item.x === pos.x && item.y === pos.y) {
                    match = true;
                    return false;
                }
            });
            return match;
        };
        if (hit(pos_tr)) {
            tr.attr('src', 'images/selectionring.png');
        } else {
            tr.attr('src', 'images/arrow_tr.png');
        }
        if (hit(pos_tl)) {
            tl.attr('src', 'images/selectionring.png');
        } else {
            tl.attr('src', 'images/arrow_tl.png');
        }
        if (hit(pos_br)) {
            br.attr('src', 'images/selectionring.png');
        } else {
            br.attr('src', 'images/arrow_br.png');
        }
        if (hit(pos_bl)) {
            bl.attr('src', 'images/selectionring.png');
        } else {
            bl.attr('src', 'images/arrow_bl.png');
        }
        tr.css('right', pos_tr.x + 'px');
        tr.css('bottom', pos_tr.y + 'px');
        tl.css('right', pos_tl.x + 'px');
        tl.css('bottom', pos_tl.y + 'px');
        br.css('right', pos_br.x + 'px');
        br.css('bottom', pos_br.y + 'px');
        bl.css('right', pos_bl.x + 'px');
        bl.css('bottom', pos_bl.y + 'px');
    });
    var body = $('body');
    body.append(player).append(tr).append(tl).append(br).append(bl);
    $('.arrow').css('position', 'absolute');
    moveWisp({
        x: data['character']['x'],
        y: data['character']['y']
    });
    $.get('locations',{},loadInteractions);
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

