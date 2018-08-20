
var cont = document.getElementById('container');


// var len = idlist.length;
var counter = 0;
var player;
function appear(){

	cont.innerHTML = innerH;
	var info = document.getElementById('info');
	var image = document.getElementById('pict');
	var countelem = document.getElementById('counter');
	var color = "rgba(" + coloravgs[0]+",0.1)";
	//alert(color);
	cont.style.visibility = "visible";
	document.getElementById('above').outerHTML = "";
	document.getElementById('top').outerHTML = "";
	document.getElementById('playlistname').innerHTML = document.getElementById('click').innerHTML;
	document.getElementById('playlistname').style.fontSize = "1rem";

	document.getElementById('click').innerHTML = '"'+ name+ '"';
	document.getElementById('click').style.fontWeight = "900";
	
	if (error){
		
		document.getElementById('spanonerror').outerHTML = "";
	}
	else{
		document.getElementById('spanwoerror').outerHTML = "";
	}

	cont.style.backgroundColor = color; 
	info.style.backgroundColor = color; 
	info.innerHTML = namelist[0];
	document.getElementById('player').style.backgroundColor = color; 
	// document.getElementById('image').style.backgroundColor = "rgb(" + coloravgs[0]+",0.1)"; 
	document.getElementById('image').style.backgroundColor = color;
	document.getElementById('buttons').style.backgroundColor = color;
	countelem.style.backgroundColor = color;
	image.src = imageurls[0];
	image.style.border = "0.5rem solid rgba(" + coloravgs[0] + ",0.6)"; 
	countelem.innerHTML = "Song " +(counter + 1) +"/" + idlist.length;

	player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: idlist[0],
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange,
      // 'onError' : errorEvent
    }
  });
}