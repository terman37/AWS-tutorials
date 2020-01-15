# Use AWS Rekognition

## Use case:

- html webpage to take a picture using webcam or file upload button

- upload picture to S3 bucket
- use facial analysis to extract attributes from pictures (show it)
- use face comparison to compare with previous image and check if same face is on picture



## Architecture:

- front end web server using nginx: 

  - t2.micro ubuntu server 18.04 ami
  - index.html / static (with css, js files)

- backend processing using flask:

  - t2.micro ubuntu server 18.04 ami
  - rekognition api use of images

  

