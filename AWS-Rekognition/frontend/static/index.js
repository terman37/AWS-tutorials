var backendip = '34.238.190.11'

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

function take_snapshot() {
    // take snapshot and get image data
    Webcam.snap(
        function(data_uri) {
            // display results in page
            $('#screenshot').html('<img src="'+data_uri+'"/>');

            $.post(
                'http://'+backendip+':5000/get_picture',
                data_uri,
                result_f,
                'html'
            );
//            function result_f(data_back){
//                $('#results').html(data_back);
//            }
        }
    );
}

function rekognize() {


}