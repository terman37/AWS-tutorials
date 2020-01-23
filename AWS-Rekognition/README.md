# Use AWS Rekognition



## Use case:

- html webpage to take a picture using webcam
- upload picture to S3 bucket
- use facial analysis to extract attributes from pictures (show it)
- keep up to 5 pictures in collection
- check for each screenshot if it exists in collection



## Architecture:

- front end web server using **nginx**: 

  - t2.micro ubuntu server 18.04 ami
  - index.html / static (with css, js files)

- backend processing using **flask**:

  - t2.micro ubuntu server 18.04 ami
  - rekognition api use of images

  

## Setup Frontend server

- Security group: open port 22 and 80.

- Install nginx server

  ```bash
  sudo apt update
  sudo apt install nginx
  ```

- clone github repository

  ```
  git clone https://github.com/terman37/AWS-tutorials.git
  ```

- change default nginx server config

  ```bash
  sudo rm /etc/nginx/sites-enabled/default
  sudo cp ~/AWS-tutorials/AWS-Rekognition/frontend/frontend.com.conf /etc/nginx/sites-enabled/
  sudo nginx -s reload
  ```

  #### Trick (allow insecure website to use webcam in chrome)

  - navigate to:

    > chrome://flags/#unsafely-treat-insecure-origin-as-secure

  - enable feature and add public ip adress of frontend server

    <img src="chrome_webcam.png" alt="chrome_webcam" style="zoom:50%;" />

- modify backend ip adress in index.js (1st line in script)

  ```
  nano ~/AWS-tutorials/AWS-Rekognition/frontend/static/index.js
  ```

  


## Setup Backend Server

- Security group: open port 22 and 5000.

- install miniconda:

  ```bash
  sudo apt update
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  sh Miniconda3-latest-Linux-x86_64.sh
  ```

- exit and reconnect to ssh

- create virtual environment (named flask)

  ```bash
  conda create -n flask python=3.7
  conda activate flask
  ```

- install Flask

  ```bash
  pip install Flask
  pip install flask_cors
  pip install boto3
  ```

- clone github repository

  ```bash
  git clone https://github.com/terman37/AWS-tutorials.git
  ```

- setup AWS credentials for boto3

  ```
  mkdir ~/.aws
  ```
  
  ```bash
  nano ~/.aws/credentials
  ```
  
  - should look like this: copy your credentials (from vocareum in my case)
  
    ```
    [default]
    aws_access_key_id=...
    aws_secret_access_key=...
    aws_session_token=...
    ```
  
  ```bash
  nano ~/.aws/config
  ```
  
  - should look like this:
  
    ```
    [default]
    region = us-east-1
    ```

- run Flask app

  ```bash
  python ~/AWS-tutorials/AWS-Rekognition/backend/myapp.py
  ```



## Test it !

- before to launch:

  - update credentials:

    ```bash
    nano ~/.aws/credentials
    ```

  - put backent IP in index.js

    ```bash
    nano ~/AWS-tutorials/AWS-Rekognition/frontend/static/index.js
    ```

  - put frontend IP in chrome to allow webcam

    > chrome://flags/#unsafely-treat-insecure-origin-as-secure
  
  - do not forget to launch Flask test server
  
    ```
    conda activate flask
    python ~/AWS-tutorials/AWS-Rekognition/backend/myapp.py
    ```
  
    

- Test frontend access in chrome at [http://Frontend-PublicIP](http://<PublicIP>)

  should look like this: except the face :-)

<img src="frontend_result.png" alt="frontend_result" style="zoom:33%;" />