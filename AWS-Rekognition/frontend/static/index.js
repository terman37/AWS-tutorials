
var backendip = '18.207.158.88'

function start_page(){
    $('#btnkeep').hide();
    $('#btnresetcol').hide();
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
    $('#btnresetcol').show();
}

function keepface(){
    var canvas;
    var id5;
    for (i = 5; i > 0; i--){
        try {
            source_canvas = document.getElementById("k"+(i-1));
            canvas = document.getElementById("k"+i);
            context = canvas.getContext("2d");
            context.drawImage(source_canvas, 0, 0,160,120);
            if (i==5){
                id5 = source_canvas.attributes.FaceId.value;
            }
            canvas.setAttribute("FaceId", source_canvas.attributes.FaceId.value);
        } catch(err) {
            console.log(err);
        }
    }
    context = source_canvas.getContext("2d");
    var data_uri = canvas.toDataURL();

    var params = "image="+data_uri;
    params += "&id5="+id5;

    $.post(
            'http://'+backendip+':5000/add_to_collection/',
            params,
            result_f,
            'html'
        );
    function result_f(data_back){
        canvas = document.getElementById("k1");
        canvas.setAttribute("FaceId", data_back);
//        for (i = 5; i > 0; i--){
//            canvas = document.getElementById("k"+i);
//            console.log("k" + i + ":" + canvas.attributes.FaceId.value);
//        }
    }

}

function resetcol(){
    var param = ""
    $.post(
            'http://'+backendip+':5000/resetcollection/',
            param,
            result_f,
            'html'
        );
    function result_f(data_back){
        console.log(data_back)
    }
    for (i = 5; i > 0; i--){
        canvas = document.getElementById("k"+i);
        context.clearRect(0, 0, 160, 120);
        canvas.setAttribute("FaceId", "0");
    }
}