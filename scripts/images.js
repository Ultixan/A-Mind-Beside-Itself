	function choice(arr){
		var c = arr.length;
		var f = Math.random();
		var i = Math.floor(c*f);
		return arr[i];	
	}
	function getImage(){
		var suits=new Array();
		suits[0]='wands';
		suits[1]='cups';
		suits[2]='swords';
		suits[3]='coins';
		var people=new Array();
		people[0]='king';
		people[1]='queen';
		people[2]='knight';
		people[3]='page';
		return '<img class="image" src="res/'+choice(people)+'of'+choice(suits)+'.png">';
	}
	function animateImage()
	{
			$("#imgloader").hide();
			$("#imgloader").fadeTo("slow", 1);
			$("#imgloader").animate({visible:true}, 2000);
			$("#imgloader").fadeTo("slow", 0);
			$("#imgloader").animate({visible:false}, 2000, loadImage);
	}
	function loadImage()
		{
		$("#imgloader").html(getImage());
	}

