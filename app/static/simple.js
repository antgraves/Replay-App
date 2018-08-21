

// function change() {
// 	document.getElementById("demo").innerHTML =  myFunction();
// }]

var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];

firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
var newcolor;

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.

// var counter = 0;


// function onYouTubeIframeAPIReady() {
// 	alert(idlist[counter])
//   player = new YT.Player('player', {
//     height: '390',
//     width: '640',
//     videoId: idlist[counter],
//     events: {
//       'onReady': onPlayerReady,
//       'onStateChange': onPlayerStateChange,
//       // 'onError' : errorEvent
//     }
//   });
// }

// function errorEvent(event) {
// 	document.getElementById("this").innerHTML = event.data;

// }
function update(){
	var countelem = document.getElementById('counter');
	var info = document.getElementById('info');
	var image = document.getElementById('pict');
	newcolor = "rgba(" + coloravgs[counter]+",0.2)";
	cont.style.backgroundColor = newcolor; 
	info.style.backgroundColor = newcolor; 
	info.innerHTML = namelist[counter];
	document.getElementById('player').style.backgroundColor = newcolor; 
	document.getElementById('image').style.backgroundColor = newcolor; 
	document.getElementById('buttons').style.backgroundColor = newcolor; 
	image.src = imageurls[counter];
	image.style.border = "0.5rem solid rgba(" + coloravgs[counter] + ",0.6)"; 
	countelem.innerHTML = "Song " +(counter + 1) +"/" + idlist.length;
	countelem.style.backgroundColor = newcolor;
	//alert(countelem.style.backgroundColor);
}
function next() {
	counter = counter + 1;
	if( counter == idlist.length){
		counter = 0;
	}
	// var str = idlist[counter];
	// var sub = str.substring(str.indexOf(" |Artist|: ") + 11) + " - " + str.substring(str.indexOf(" |Track|: ") + 10, str.indexOf(" |Artist|: "));
	// document.getElementById("this").innerHTML =  sub;
	// document.getElementById("demo").innerHTML =  "Song " + (counter + 1) + "/" + len;
	update();
	player.loadVideoById({videoId:idlist[counter],
                      startSeconds:0,
                      suggestedQuality:'large'});
	
   // document.getElementById("demo").innerHTML =  {{ output|tojson }};
}
function previous() {
	counter = counter - 1
	if( counter < 0){
		counter = idlist.length - 1;
	}
	// var str = outputTracks[counter];
	// var sub = str.substring(str.indexOf(" |Artist|: ") + 11) + " - " + str.substring(str.indexOf(" |Track|: ") + 10, str.indexOf(" |Artist|: "));
	// document.getElementById("this").innerHTML =  sub;
	// document.getElementById("thepic").src = outputImages[counter];
	// alert(outputImages[counter]);
	//document.getElementById("demo").innerHTML =  "Song " + (counter + 1) + "/" + len;
	update();
	player.loadVideoById({videoId:idlist[counter],
                      startSeconds:0,
                      suggestedQuality:'large'});
	
   // document.getElementById("demo").innerHTML =  {{ output|tojson }};
}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
   event.target.playVideo();
}

// 5. The API calls this function when the player's state changes.
//    The function indicates that when playing a video (state=1),
//    the player should play for six seconds and then stop.
var done = false;
function onPlayerStateChange(event) {
  // if (event.data == YT.PlayerState.PLAYING && !done) {
  //   setTimeout(stopVideo, 6000);
  //   done = true;
  // }
}
function stopVideo() {
  player.stopVideo();
}