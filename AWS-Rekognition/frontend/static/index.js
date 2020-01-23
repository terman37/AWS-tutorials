
var backendip = '35.174.61.191'

function set_webcam(){
    Webcam.set(
        {
            width: 320,
            height: 240,
            image_format: 'jpeg',
            jpeg_quality: 90
        }
     );

     context.drawImage(video, 0, 0, 640, 480)

    Webcam.attach('#my_camera');
}

function take_snapshot(id) {
    // take snapshot and get image data
    Webcam.snap(
        function(data_uri) {
            // display results in page
            $('#screenshot'+id).html('<img src="'+data_uri+'"/>');
            $.post(
                'http://'+backendip+':5000/get_picture'+id+'/',
                data_uri,
                result_f,
                'html'
            );
            function result_f(data_back){
                $('#results'+id).html($.parseHTML(data_back));
            }
        }
    );
}

function rekognize() {

    var pic1 = $('#screenshot1').contents().length
    var pic2 = $('#screenshot1').contents().length

    if(pic1>0 && pic2>0){
        $.post(
            'http://'+backendip+':5000/compare/',
            "nothing",
            result_f,
            'html'
        );
        function result_f(data_back){
            $('#compare').html($.parseHTML(data_back));
        }
    }
}