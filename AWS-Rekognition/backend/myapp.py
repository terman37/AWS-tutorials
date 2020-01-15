from flask import Flask, request
from flask_cors import CORS
from urllib.request import urlopen
from binascii import a2b_base64

app = Flask(__name__)
CORS(app) #added by me

@app.route("/get_picture/", methods=['GET', 'POST'])
def getpicture():
    imgData = str(request.get_data())
    imgData64 = imgData[imgData.find(',')+1:]
    binary_data = a2b_base64(imgData64)
    with open('image.jpg', 'wb') as fd:
        fd.write(binary_data)

    return "Hello, World!"

if __name__ == "__main__":
    # run the app locally on the given port
    app.run(host='0.0.0.0', port=5000)