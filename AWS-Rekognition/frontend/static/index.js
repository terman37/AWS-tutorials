
var backendip = '3.80.232.151'

function start_page(){
    $('#btnkeep').hide();
    $('#btnresetcol').hide();
    resetcol()
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
    $('#btnkeep').hide();
    var canvas = document.getElementById("k0");
	context = canvas.getContext("2d");
	video = document.getElementById("webcam_live");
    context.drawImage(video, 0, 0,320,240);
    var data_uri = canvas.toDataURL();
    $.post(
            'http://'+backendip+':5000/get_picture/',
            data_uri,
            result_f,
            'json'
        );
    function result_f(data_back){
        $('#results').html($.parseHTML(data_back.answer));

        canvas = document.getElementById("k0");
        context = canvas.getContext("2d");
        context.beginPath();
        context.lineWidth = "3";
        context.strokeStyle = "red";
        context.rect(data_back.bbox.Top, data_back.bbox.Left, data_back.bbox.Width, data_back.bbox.Height);
        context.stroke();

        if (data_back.similar != 0){
            $("#similar").html("Similarity: <kbd>" + data_back.similar + "%</kbd>");
            for (i = 5; i > 0; i--){
                canvas = document.getElementById("k"+i);
                if (canvas.attributes.FaceId.value == data_back.faceid){
                    console.log("match at "+i);
                    $("#k"+i).parent().removeClass("bg-success").addClass("bg-success");
                } else {
                    $("#k"+i).parent().removeClass("bg-success");
                }
                console.log("k" + i + ":" + canvas.attributes.FaceId.value);
            }
        } else {
            $("#similar").html("");
            for (i = 5; i > 0; i--){
                $("#k"+i).parent().removeClass("bg-success");
            }
        }

        canvas = document.getElementById("k5");
        if (canvas.attributes.FaceId.value != 0){
            $('#results').prepend("<p>Not possible to add more faces  --> Reset Collection</p>");
        } else {
            if (data_back.similar == 0){
                $('#btnkeep').show();
            }
        }
    }

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
            try{
                canvas.setAttribute("FaceId", source_canvas.attributes.FaceId.value);
            } catch(err) {
                console.log(i + "//" + err)
            }
        } catch(err) {
            console.log(i + "//" + err);
        }
    }

    canvas = document.getElementById("k0");
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
//        for (i = 5; i > 0; i--){
//            canvas = document.getElementById("k"+i);
//            console.log("k" + i + ":" + canvas.attributes.FaceId.value);
//        }
        canvas = document.getElementById("k0");
        context = canvas.getContext("2d");
        context.clearRect(0, 0, 320, 240);
        canvas.setAttribute("FaceId", "0");

        $('#btnkeep').hide();
        $('#btnresetcol').show();
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
        $('#btnresetcol').hide();
    }
    for (i = 5; i > 0; i--){
        canvas = document.getElementById("k"+i);
        context = canvas.getContext("2d");
        context.clearRect(0, 0, 160, 120);
        canvas.setAttribute("FaceId", "0");
        $("#k"+i).parent().removeClass("bg-success");
    }
//    canvas = document.getElementById("k0");
//    context = canvas.getContext("2d");
//    context.clearRect(0, 0, 320, 240);

    $("#similar").html("");
    $('#results').html("");

}