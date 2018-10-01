var topbuttons = document.getElementsByClassName('buttonup');
var botbuttons = document.getElementsByClassName('buttondown');
var data = new FormData(); //form to submit to python file
var topone;
var bottomone;
function buttonpush(id, buttons){ //highlight selected buttons, remove highlight from non-selected buttons
  for (var j = 0; j < 3; j++){
    if(id == buttons[j].id){

 document.getElementById(buttons[j].id).style.outline = "0.2rem solid blue";

      if(id == 'spotify' || id == 'spotify2'){
  document.getElementById(buttons[j].id).style.backgroundColor = "rgb(0, 168, 73)";
        
      }
      else if(id == 'tidal' || id == 'tidal2'){
        document.getElementById(buttons[j].id).style.backgroundColor = "black";
        
      }
       else if(id == 'youtube'){
         document.getElementById(buttons[j].id).style.backgroundColor = "rgb(196,0,0)";
       }
      else if (id == 'apple'){
        document.getElementById(buttons[j].id).style.background = "linear-gradient(to right, rgb(115,0,180), rgb(192,0,78))";
      }
      if(buttons == topbuttons){
        
        data.set("top",buttons[j].id );
        document.getElementById('top').value =buttons[j].id; 
       
      }
      else {
        
        data.set("bottom",buttons[j].id.substring(0,buttons[j].id.length - 1) );
        document.getElementById('bottom').value =buttons[j].id.substring(0,buttons[j].id.length - 1) ; 
        
      }
    
    }
    
    else{   
      document.getElementById(buttons[j].id).style.backgroundColor = null;
    document.getElementById(buttons[j].id).style.outline = null;
         document.getElementById(buttons[j].id).style.background = null;
              
    } }
  }
for (var i=0 ; i < topbuttons.length ; i++){
  (function(ind){
    topbuttons[ind].onclick = function(){
      buttonpush(topbuttons[ind].id,topbuttons);
    };})(i) }

for (var i=0 ; i < botbuttons.length ; i++){
    (function(ind){
      botbuttons[ind].onclick = function(){
        buttonpush(botbuttons[ind].id,botbuttons);
      };})(i) }

function addSubmit(ev) { //don't submit form if error in user input

  var errpresent = errCheck();
  
  if(errpresent.length != 0){
      ev.preventDefault();
  document.getElementById('error').innerHTML = errpresent;
  }
    }
 
  var form = document.getElementById('form');
    
  form.addEventListener('submit', addSubmit); //on form submission

function errCheck(){ //check for errors in user submission
  
  var url = document.getElementById("url").value;
  var retstring = compErrCheck(url);
  if (url.length == 0){
     return "Please enter a url"; 
  }
 
  var top = data.get('top');
  var bottom = data.get('bottom');
  if (top == null){
    return "Select a service from above"
  }
  if (bottom == null){
    return "Select a service from below"
  }
  if (top == bottom ){
    return "Select two different services";
  }
  
  return retstring;
}
function compErrCheck(url){
  if (! url.toLowerCase().includes(data.get('top') ) && url.length > 0) {
    return "Url does not match streaming service";
  }
  return "";
  
  
  
}












