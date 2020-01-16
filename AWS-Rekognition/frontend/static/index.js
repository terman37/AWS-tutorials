var backendip = '3.215.77.208'

function set_webcam(){
    Webcam.set(
        {
            width: 320,
            height: 240,
            image_format: 'jpeg',
            jpeg_quality: 90
        }
     );
    Webcam.attach('#my_camera');
}

function take_snapshot(destin = 'get_picture/') {
    // take snapshot and get image data
    Webcam.snap(
        function(data_uri) {
            // display results in page
            if(destin == 'get_picture/') {
                $('#screenshot').html('<img src="'+data_uri+'"/>');
            } else {
                $('#screenshot2').html('<img src="'+data_uri+'"/>');
            }
            $.post(
                'http://'+backendip+':5000/'+destin,
                data_uri,
                result_f,
                'html'
            );
            function result_f(data_back){
                $('#results').html($.parseHTML(data_back));
            }
        }
    );
}

function rekognize() {
    take_snapshot(destin = 'compare/')
}