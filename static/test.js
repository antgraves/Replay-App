   var topbuttons = document.getElementsByClassName('buttonup');
var botbuttons = document.getElementsByClassName('buttondown');
var data = new FormData();
var topone;
var bottomone;
function buttonpush(id, buttons){
  for (var j = 0; j < 3; j++){
    if(id == buttons[j].id){
    document.getElementById(buttons[j].id).style.filter = "brightness(70%)";
      if(buttons == topbuttons){
        data.set("top",buttons[j].id );
        topone = buttons[j].id;
        // alert(data.get('bottom'));
      }
      else {
        data.set("bottom",buttons[j].id.substring(0,buttons[j].id.length - 1) );
        bottomone = buttons[j].id.substring(0,buttons[j].id.length - 1);
      }
      // alert("I am button " + buttons[j].id)
    }
    
    else{     document.getElementById(buttons[j].id).style.filter = null;
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
    return "Select two different options";
  }
  
  return retstring;
}
function compErrCheck(url){
  if (! url.toLowerCase().includes(data.get('top') ) && url.length > 0) {
    return "Url does not match streaming service";
  }
  return "";
  
  
  
}












