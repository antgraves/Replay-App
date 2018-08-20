
	var misses = [];
	var miss = ["Test"];
	var bardone = false;
	var source = new EventSource("/progress");
	var count = 0;
	var len = 0;
	var url = "";
	var ls = document.getElementById('olist');
	var name = "";
	var urlstat = true;
	var error = false;
	var imageimp = false;
	var imageurls = [];
	var coloravgs = [];
	var imgbool = true;
	var idlist = [];
	var idstart = false;
	var namelist = [];
	var youtube = bgcolor == "youtub";
	var addsongs = false;

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
		document.getElementById('click').style.visibility = "visible";
		document.getElementById('load').style.visibility = "hidden";
		
		//alert(ls);
		if (misses.length == 0){
			document.getElementById('above').innerHTML = "All songs from the submitted playlist were added";
			
		}
		else{
			if(bgcolor == "tidal"){
			document.getElementById('above').innerHTML = 'The following songs could not be added to "My Music" :';
			document.getElementById('disc').innerHTML = 'The songs from playlist "' + name + '" were added to the "My Music" section of your Tidal account.'
		}
			else{
			document.getElementById('above').innerHTML = 'The following songs could not be added to the playlist:';
			}
}
	}
	source.onmessage = function(event) {
		alert(event.data);
		if(event.data == "!!||ERROR||!!"){
			document.getElementById('click').innerHTML = "Error - Could not create YouTube Playlist";
			document.getElementById('click').style.visibility = "visible";
			error = true;
			source.close();
			// alert(imageurls);
			// alert(coloravgs);
			// alert(namelist);

			
		}

		if ((event.data.substring(0,5) == 'https' || event.data.substring(0,2)== '{[') && !bardone && youtube){
			alert('we here');
			if(imgbool){
				imageurls.push(event.data);
				imgbool = false;
			}
			else{
				//alert('here');
				//alert(event.data);
				coloravgs.push(event.data);
				imgbool = true;
			}
		}
		if((event.data.substring(0,1)== '[' && youtube) || idstart){
			if(!idstart){
				len = Number(event.data.substring(1));
				
				idstart = true;
			}
			else if(count < len){
				idlist.push(event.data);
				//alert(misses);	
				count += 1;
				// alert(count);
				}

			else{
				//alert(event.data);
				name = event.data;
				idstart = false;
				
			}
			//alert(len);
		}
		
		else if(youtube && event.data == '100'){
			bardone = true;
			$('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
			$('.progress-bar-label').text(event.data+'%');

		}

		else if((event.data.substring(0,1)== '[' && !youtube) || (bardone && !error && !imageimp && !youtube)){
			console.log('issa where');
			if(!bardone){
				console.log('issa there');
				len = Number(event.data.substring(1));
				
				bardone = true;
			}
			else if(count < len){
				console.log('issa here');
				misses.push(event.data);
				//alert(misses);	
				count += 1;
				// alert(count);
				}
			else if (event.data.substring(0,5) == 'https' && urlstat)
			{
				url = event.data;
				urlstat = false;
				//alert(url);
			}

			

			else{
				//alert(event.data);
				name = event.data;
				source.close();
				unHide();
				genList();
				}
				
			
			//alert(len);
		}
		if(!youtube){
			console.log('yeaaa boiii')
		}
		if(bardone && youtube && event.data.substring(0,5) == 'https'){
			url = event.data;
		}
		if(youtube && event.data.indexOf(' - ') > -1){
			namelist.push(event.data);
		}
		if(!bardone &&  !error && event.data.substring(0,5) != 'https' && event.data.substring(0,1) != '[' && event.data.indexOf('-') <= -1){
			$('.progress-bar').css('width', event.data+'%').attr('aria-valuenow', event.data);
			$('.progress-bar-label').text(event.data+'%');
			// addsongs = false;
		}

		
		
		if (bardone && imageimp && !idstart && imgbool && event.data == 'Complete')
		{
			alert(imageurls);
			alert(coloravgs);
			source.close();
			unHide();
			genList();
		}
	}
		