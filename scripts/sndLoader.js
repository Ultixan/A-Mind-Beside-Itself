function choice(arr){
	var c = arr.length;
	var f = Math.random();
	var i = Math.floor(c*f);
	return arr[i];
};

function setupSounds(){
	var t=setTimeout("playSound(chooseSound())", random_interval());
};
function random_interval(){
	var start = 15000;
	var f=Math.random();
	start = start + 5000*f;
	return Math.floor(start);
};
function chooseSound(){
	var sounds = new Array();
	sounds[0] = 'horn-sound';
	sounds[1] = 'mindthegap-sound';
	sounds[2] = 'pa-sound';
	sounds[3] = 'train-sound';
	return choice(sounds);
};
function playSound(id){
	document.getElementById(id).play();
};
