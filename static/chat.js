var me = {};
me.avatar = "../static/avatar.png";

var you = {};
you.avatar = "../static/therapist.png";

function insert_chat(who, text) {
  var control = "";
  if (who == "me") {
    control =
      '<li class="message right appeared">' +
      '<div class="avatar"><img class="img-circle" style="width:100%;" src="' +
      me.avatar +
      '" /> </div>' +
      '<div class="text_wrapper">' +
      '<div class="text">' +
      text +
      "</div>" +
      "</div>" +
      "</li>";
  } else {
    control =
      '<li class="message left appeared">' +
      '<div class="avatar"><img class="img-circle" style="width:100%;" src="' +
      you.avatar +
      '" /> </div>' +
      '<div class="text_wrapper">' +
      '<div class="text">' +
      text +
      "</div>" +
      "</div>" +
      "</li>";
  }
  setTimeout(function() {
    $("#ul_input")
      .append(control)
      .scrollTop($("#ul_input").prop("scrollHeight"));
  });
}

function interact(message) {
  console.log("STARTING");
  $.ajax({
    type: "POST",
    url: "/senti",
    contentType: "application/json; charset = utf-8",
    dataType: "json",
    data: message,
    success: function(data) {
      insert_chat("you", data["text"]);
    }
  });
}

function get_message() {
  var message = document.getElementById("text_message").value;
  var json_data = { msg: message };
  var sender = JSON.stringify(json_data);
  console.log(sender);
  console.log(message);
  insert_chat("me", message);
  interact(sender);
}

function get_audio() {
  $.ajax({
    type: "POST",
    url: "/audio",
    context: "application/json",
    dataType: "json"
  }).done(function() {
    insert_chat("me", message);
    interact(sender);
  });
}

function startDictation() {
  if (window.hasOwnProperty("webkitSpeechRecognition")) {
    var recognition = new webkitSpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.lang = "en-US";
    recognition.start();

    recognition.onresult = function(e) {
      document.getElementById("text_message").value =
        e.results[0][0].transcript;
      recognition.stop();
      document.getElementById("text_message").submit();
    };

    recognition.onerror = function(e) {
      recognition.stop();
    };
  }
}
