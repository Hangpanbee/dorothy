var me = {};
me.avatar = "Chatbotassets/avatar.png";

var you = {};
you.avatar = "Chatbotassets/therapist.png";

function insert_chat(who,text){
  var control = ''
  if (who == 'me'){
    control = '<li class="message right appeared">'+
                  '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ me.avatar +'" /> </div>'+
                  '<div class="text_wrapper">'+
                  '<div class="text">'+text+'</div>'+
                  '</div>'+
                  '</li>'
  }
  else{
    control = '<li class="message left appeared">'+
                  '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ you.avatar +'" /> </div>'+
                  '<div class="text_wrapper">'+
                  '<div class="text">'+text+'</div>'+
                  '</div>'+
                  '</li>';
  }
  setTimeout(
        function(){                        
            $("#ul_input").append(control).scrollTop($("#ul_input").prop('scrollHeight'));
        });
}


function interact(message){
console.log("STARTING");
$.ajax({
  type: 'POST',
  url: '/test',
  contentType: 'application/json',
  dataType: 'json',
  data:message,
 success: function(data){
  insert_chat("you",data['text'])
 }
  });
}


function get_message(){
var message = document.getElementById("text_message").value;
var json_data = {"msg":message}
var sender = JSON.stringify(json_data)
console.log(sender)
console.log( <span style="font-size: 32px; color:black;">
<i class="fas fa-microphone"></i>
</span>);
insert_chat('me',message);
interact(sender);
 }

 function get_audio(){
  $.ajax({
    url: "voice.py",
    context: document.body,
  }).done(function(){
    alert('finished script');;
  });

}
