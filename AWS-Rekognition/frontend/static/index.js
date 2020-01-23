
var backendip = '18.207.158.88'

function start_page(){
    var video = document.querySelector("#webcam_live");
    if (navigator.mediaDevices.getUserMedia) {
        var constraints = { video: true }
        navigator.mediaDevices.getUserMedia(constraints)
            .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (err0r) {
          console.log("Something went wrong!");
        });
    }
}

function snap(){
    var canvas = document.getElementById("snapshot");
	context = canvas.getContext("2d");
	video = document.getElementById("webcam_live");
    context.drawImage(video, 0, 0,320,240);
    var data_uri = canvas.toDataURL();
    $.post(
            'http://'+backendip+':5000/get_picture/',
            data_uri,
            result_f,
            'html'
        );
    function result_f(data_back){
        $('#results'+id).html($.parseHTML(data_back));
    }
}
