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
            $('#results').html('<img src="'+data_uri+'"/>');
        }
    );
}

function rekognize() {


}