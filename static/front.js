var topbuttons = document.getElementsByClassName('buttonup');
var botbuttons = document.getElementsByClassName('buttondown');

function buttonpush(id, buttons){
  for (var j = 0; j < 3; j++){
    if(id == buttons[j].id){
    document.getElementById(buttons[j].id).style.filter = "brightness(70%)";
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


