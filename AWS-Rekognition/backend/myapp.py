from flask import Flask, request
from flask_cors import CORS
import urllib

app = Flask(__name__)
CORS(app) #added by me

@app.route("/get_picture/", methods=['GET', 'POST'])
def getpicture():
    imgData = request.get_data()
    response = urllib.request.urlopen(imgData)
    with open('image.jpg', 'wb') as f:
        f.write(response.file.read())
    return "Hello, World!"

if __name__ == "__main__":
    # run the app locally on the given port
    app.run(host='0.0.0.0', port=5000)