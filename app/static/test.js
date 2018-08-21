   var topbuttons = document.getElementsByClassName('buttonup');
var botbuttons = document.getElementsByClassName('buttondown');
var data = new FormData();
var topone;
var bottomone;
function buttonpush(id, buttons){
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
        topone = buttons[j].id;
       
      }
      else {
        
        data.set("bottom",buttons[j].id.substring(0,buttons[j].id.length - 1) );
        bottomone = buttons[j].id.substring(0,buttons[j].id.length - 1);
        
      }
      // alert("I am button " + buttons[j].id)
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

function addSubmit(ev) {

  var errpresent = errCheck();
  
  if(errpresent.length != 0){
      ev.preventDefault();
  document.getElementById('error').innerHTML = errpresent;
  }
   
      var request = new XMLHttpRequest();
      // request.addEventListener('load', consolee);
      request.open('POST', url);
      sd = new FormData(this);
      sd.set("top", topone);
      sd.set("bottom", bottomone);
      request.send(sd);
      // request.send(data);
      // console.log('submitted');
    }

function addShow() {
    }
    function consolee() {
      console.log("clicked");
    }
     
    var form = document.getElementById('form');
    
    form.addEventListener('submit', addSubmit);

function errCheck(){
  
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












