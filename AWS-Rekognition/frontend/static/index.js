
var backendip = '18.207.158.88'

function start_page(){
    $('#btnkeep').hide();
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
    var canvas = document.getElementById("k0");
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
        $('#results').html($.parseHTML(data_back));
    }
    $('#btnkeep').show();
}

function keepface(){
    var canvas;
    for (i = 5; i > 0; i--){
        try {
            source_canvas = document.getElementById("k"+(i-1));
            canvas = document.getElementById("k"+i);
            context = canvas.getContext("2d");
            context.drawImage(source_canvas, 0, 0,160,120);
            canvas.setAttribute("FaceId", source_canvas.attributes.FaceId)
        } catch(err) {
            console.log(err)
        }
    }
    context = source_canvas.getContext("2d");
    var data_uri = canvas.toDataURL();
    $.post(
            'http://'+backendip+':5000/add_to_collection/',
            data_uri,
            result_f,
            'html'
        );
    function result_f(data_back){
        canvas = document.getElementById("k1");
        canvas.setAttribute("FaceId", data_back);
        for (i = 5; i > 0; i--){
            console.log("k" + i + ":" + canvas.attributes.FaceId.value);
        }
    }


}