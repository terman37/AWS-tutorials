from flask import Flask, request
from flask_cors import CORS
from binascii import a2b_base64
import boto3
import json

app = Flask(__name__)
CORS(app)  # added by me

@app.route("/get_picture/", methods=['GET', 'POST'])
def getpicture():
    rdata = request.get_data()
    image_name = 'image1.jpg'
    save_uri_as_jpeg(rdata, image_name)
    print("screenshot saved as %s" % image_name)

    # Upload in S3 bucket
    upload_to_S3(image_name)

    # Launch Reko detect faces...
    myjson = AWSdetect_faces(image_name)

    # Extract Json infos
    answer = get_features_from_json(myjson)

    return answer


@app.route("/compare/", methods=['GET', 'POST'])
def comparepicture():
    answer = AWScomparefaces()
    print(answer)
    return answer


def save_uri_as_jpeg(uri, imagename):
    imgData = str(uri)
    imgData64 = imgData[imgData.find(',') + 1:]
    binary_data = a2b_base64(imgData64)
    with open(imagename, 'wb') as fd:
        fd.write(binary_data)


def upload_to_S3(imagename):
    mys3 = boto3.resource('s3')
    mybucket = mys3.Bucket('images-for-reko')
    myobject = mybucket.Object(imagename)
    myobject.delete()
    myobject.wait_until_not_exists()
    print("deleted")
    myobject.upload_file(imagename)
    myobject.wait_until_exists()
    print("uploaded")


def AWSdetect_faces(imagename):
    reko = boto3.client('rekognition')
    response = reko.detect_faces(
        Image={
            'S3Object': {
                'Bucket': 'images-for-reko',
                'Name': imagename,
            }
        },
        Attributes=[
            'ALL',
        ]
    )
    return response


def AWScomparefaces():
    reko = boto3.client('rekognition')

    response = reko.compare_faces(
        SourceImage={
            'S3Object': {
                'Bucket': 'images-for-reko',
                'Name': 'image1.jpg',
            }
        },
        TargetImage={
            'S3Object': {
                'Bucket': 'images-for-reko',
                'Name': 'image2.jpg',
            }
        },
        SimilarityThreshold=90,
        QualityFilter='AUTO'
    )

    FaceMatch = response['FaceMatches']
    mystr = "<kbd> Similarity = "
    if len(FaceMatch) > 0:
        FirstMatch = FaceMatch[0]
        mystr += "%.2f%%" % FirstMatch['Similarity']
    else:
        mystr += "No Matching face"
    mystr += "</kbd>"
    return mystr


def get_features_from_json(myjson):
    mystr = ""
    facedetails = myjson['FaceDetails']
    nbfaces = len(facedetails)
    notusedattributes = ['BoundingBox', 'Landmarks', 'Pose', 'Quality', 'Confidence']
    if nbfaces == 1:
        face = facedetails[0]
        mystr += '<table class="table table-sm table-striped bg-light m-2">'
        for attribute, details in face.items():
            if attribute not in notusedattributes:
                mystr += '<tr>'
                if attribute == 'AgeRange':
                    mystr += "<td>%s</td><td>%d</td><td>%d yo</td>" % (attribute, details['Low'], details['High'])
                elif attribute != "Emotions":
                    mystr += "<td>%s</td><td>%s</td><td>%.2f%%</td>" % (
                    attribute, details['Value'], details['Confidence'])
                else:
                    for emotion in details:
                        if emotion['Confidence'] > 50:
                            mystr += "<td>Emotion</td><td>%s</td><td>%.2f%%</td>" % (
                            emotion['Type'], emotion['Confidence'])
                mystr += "</tr>"
        mystr += "</table>"
    elif nbfaces > 1:
        mystr += "%d faces found on picture...\n" % len(facedetails)
    else:
        mystr += "Nobody on picture...\n"
    return mystr


if __name__ == "__main__":
    # run the app locally on the given port
    app.run(host='0.0.0.0', port=5000)
