	function choice(arr){
		var c = arr.length;
		var f = Math.random();
		var i = Math.floor(c*f);
		return arr[i];	
	}
	function getImage(){
		var images=new Array();
		images[0]='<img src="res/kingofwands.png">';
		images[1]='<img src="res/pageofcups.png">';
		//When we get all the images, they'll be put here
		return choice(images);
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

