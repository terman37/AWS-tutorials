from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
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

    # Upload in S3 bucket
    upload_to_S3(image_name)

    # Launch Reko detect faces...
    myjson = AWSdetect_faces(image_name)

    # Extract Json infos
    nbfaces, bbox, answer = get_features_from_json(myjson)

    # check if face is found in collection
    similarity = 0
    faceid = '-'
    if nbfaces > 0:
        collname = create_collection_if_needded()
        nbfaces = nb_of_faces_in_collection(collname)
        if nbfaces > 0:
            similarity, faceid = find_face_in_collection(collname, image_name)

    json = {'answer': answer, 'faceid': faceid, 'similar': round(similarity, 2), 'nbfaces': nbfaces, 'bbox': bbox}

    return jsonify(json)


@app.route("/resetcollection/", methods=['GET', 'POST'])
def reset_collection():
    # Delete collection
    reko = boto3.client('rekognition')
    try:
        response = reko.delete_collection(
            CollectionId='mycollection'
        )
        return "Collection deleted ! "
    except:
        return "No Collection to delete ! "


@app.route("/add_to_collection/", methods=['GET', 'POST'])
def add_to_collection():
    rdata = request.get_data()
    image_name = 'image_for_collection.jpg'
    save_uri_as_jpeg(rdata, image_name)

    # Upload in S3 bucket
    upload_to_S3(image_name)

    # get_collection id
    collname = create_collection_if_needded()

    # Add face to Rekognition collection
    faceid = add_face_to_collection(collname, image_name)

    return faceid


@app.route("/compare/", methods=['GET', 'POST'])
def comparepicture():
    answer = AWScomparefaces()
    print(answer)
    return answer


def create_collection_if_needded():
    reko = boto3.client('rekognition')
    # check if any collection
    response = reko.list_collections(
        MaxResults=1
    )
    collid = response['CollectionIds']
    if len(collid) == 0:
        # if no collection found / create one
        collname = 'mycollection'
        res = reko.create_collection(
            CollectionId='mycollection'
        )
    else:
        collname = collid[0]
    return collname


def add_face_to_collection(collname, image_name):
    reko = boto3.client('rekognition')

    # response = reko.describe_collection(
    #     CollectionId=collname
    # )
    # if response['FaceCount'] > 1:
    #     response = reko.list_faces(CollectionId=collname)
    #     # print(response)

    # add face to collection (only main one)
    response = reko.index_faces(
        CollectionId=collname,
        Image={
            'S3Object': {
                'Bucket': 'images-for-reko',
                'Name': image_name
            }
        },
        DetectionAttributes=['DEFAULT'],
        MaxFaces=1,
        QualityFilter='AUTO'
    )

    # send back Face Id generated
    response = response['FaceRecords']
    response = response[0]
    response = response['Face']
    response = response['FaceId']

    return response


def nb_of_faces_in_collection(collname):
    reko = boto3.client('rekognition')

    response = reko.describe_collection(
        CollectionId=collname
    )
    return response['FaceCount']


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
    # as using always same name for file, delete old one before to add new one
    myobject.delete()
    myobject.wait_until_not_exists()
    myobject.upload_file(imagename)
    myobject.wait_until_exists()
    print(imagename + " uploaded")


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


def find_face_in_collection(collname, image_name):
    reko = boto3.client('rekognition')
    try:
        response = reko.search_faces_by_image(
            CollectionId=collname,
            Image={
                'S3Object': {
                    'Bucket': 'images-for-reko',
                    'Name': image_name,
                }
            },
            MaxFaces=1,
            FaceMatchThreshold=90,
            QualityFilter='AUTO'
        )
        response = response['FaceMatches']
        response = response[0]
        similarity = response['Similarity']
        response = response['Face']
        faceid = response['FaceId']
    except:
        similarity = 0
        faceid = 0

    return similarity, faceid


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
    # create details table from json response from detect faces
    mystr = ""
    bbox = {0,0,0,0}
    facedetails = myjson['FaceDetails']
    nbfaces = len(facedetails)
    notusedattributes = ['BoundingBox', 'Landmarks', 'Pose', 'Quality', 'Confidence']
    if nbfaces == 1:
        face = facedetails[0]
        bbox = face['BoundingBox']
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
    return nbfaces, bbox, mystr


if __name__ == "__main__":
    # run the app locally on the given port
    app.run(host='0.0.0.0', port=5000)
