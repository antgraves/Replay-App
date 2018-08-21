
	var misses = [];
	var source = new EventSource("/progress");
	var url = "";
	var ls = document.getElementById('olist');
	var name = "";
	var imageurls = [];
	var coloravgs = [];
	var idlist = [];
	var namelist = [];
	var youtube = bgcolor == "youtub";
	var error = false;
	var bar = document.getElementById('barMove');
	var errorurl = "";
	var click = document.getElementById('click');
	var innerH = document.getElementById('container').innerHTML;
	document.getElementById('container').innerHTML = "";
	console.log(bgcolor);
	console.log(topdiv);

	if (bgcolor == "spotify"){
		document.getElementById('above').style.backgroundColor = "#ddf9cf";
		ls.style.backgroundColor = "#ddf9cf";
	}
	if (bgcolor == "tidal"){
		document.getElementById('above').style.backgroundColor = '#e3e3e3';
		ls.style.backgroundColor = '#e3e3e3';
	}
	if (youtube){
		document.getElementById('above').style.backgroundColor = '#ffb8b8';
		ls.style.backgroundColor = '#ffb8b8';
	}

	if (topdiv == "spotify"){
		errorurl = "https://open.spotify.com/user/youruserid/playlist/...";
	}
	if (topdiv == "tidal"){
		errorurl = "https://listen.tidal.com/playlist/...";
	}
	if (topdiv == "apple"){
		errorurl = "https://itunes.apple.com/yourcountrycode/playlist/...";
	}

	function genList(){
		
		//alert('tada');
		for (var i = 0; i < misses.length; i++) {
			//alert(ls);

			var entry = document.createElement('li');
    		entry.appendChild(document.createTextNode(misses[i]));
    		//alert(document.getElementById('load'));
    		ls.appendChild(entry);
		}
    	//alert('magic');

	}
	function unHide(){
		document.getElementById('load').innerHTML="";
		document.getElementById('url').href = url;
		click.style.visibility = "visible";
		document.getElementById('load').style.visibility = "hidden";
		document.getElementById('playlistname').style.visibility = "visible";
		document.getElementById('playlistname').innerHTML = '"' + name + '" has found a new home!';
		
		//alert(ls);
		if (youtube) {
			document.getElementById('spanwoerror').style.visibility = "visible";
			document.getElementById('spanonerror').outerHTML = "";
		}
		if (bgcolor == 'tidal') {
			document.getElementById('spanonerror').innerHTML = 'The songs from playlist "' + name + '" were added to the "My Music" section of your Tidal account.'
			document.getElementById('spanonerror').style.visibility = "visible";
			document.getElementById('spanonerror').style.color = "red";
			document.getElementById('spanwoerror').outerHTML = "";
		}
		if (misses.length == 0 && !youtube){
			document.getElementById('above').innerHTML = 'All songs from "' + name + '" were added';
			ls.outerHTML = "";
			
		}

		else if (youtube) {
			ls.outerHTML = "";
		}
		else{
			ls.style.visibility = "visible";
			if(bgcolor == "tidal"){
			document.getElementById('above').innerHTML = 'The following songs could not be added to "My Music" :';
			
		}
			else{
			document.getElementById('above').innerHTML = 'The following songs could not be added to the playlist:';
			}
}
	}
	source.onmessage = function(event) {
		//console.log(event.data);

		if (event.data.substring(0,4) == "SONG"){
			namelist.push(event.data.substring(4));
		}
		else if(event.data.substring(0,5) == "IMAGE"){
			imageurls.push(event.data.substring(5));
		}
		else if(event.data.substring(0,5) == "COLOR"){
			//console.log(event.data.substring(5));
			coloravgs.push(event.data.substring(5));
		}
		else if(event.data.substring(0,3) == "IDS"){
			idlist.push(event.data.substring(3));
		}
		else if(event.data.substring(0,4) == "NAME"){
			name = event.data.substring(4);
		}
		else if(event.data.substring(0,4) == "MISS"){
			misses.push(event.data.substring(4));
		}
		else if(event.data == "ERROR"){
			// if(youtube){
			// 	document.getElementById('click').innerHTML = "Error - Could not create YouTube Playlist";
			// }
			if (bgcolor == 'tidal') {
				click.innerHTML = 'Something went wrong! Please ensure that your login details were accurate and that the playlist url is correct and is of the form ' + errorurl;
			}
			else{
				click.innerHTML = 'Something went wrong! Please ensure that the playlist url is correct and is of the form ' + errorurl;
			}
			click.style.fontSize = "1.8rem"
			click.style.visibility = "visible";
			document.getElementById('playlistname').outerHTML = '';
			source.close();
			error = true;
		}
		else if(event.data == "YTERROR"){
			click.innerHTML = "Error - Could not create YouTube Playlist";
			click.style.visibility = "visible";
			document.getElementById('spanonerror').style.visibility = "visible";
			document.getElementById('spanwoerror').outerHTML = "";
			error = true;
			ls.outerHTML = "";
			source.close();
		}
		else if(event.data.substring(0,3) == "URL"){
			url = event.data.substring(3);
		}
		else if(event.data == "COMPLETE"){
			source.close();
			unHide();
			genList();
			// alert(name);
			// alert(url);
		}
		else{
			bar.innerHTML = event.data + "%";
			bar.style.width = event.data + "%";
			// $('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
			// $('.progress-bar-label').text(event.data+'%');
		}
		// if(event.data == 'COMPLETE'){
			
		// 	alert(imageurls);
		// 	alert(coloravgs);
		// 	alert(namelist);
			
		// }

	}
		