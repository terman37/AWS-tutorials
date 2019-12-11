# AWS DataScience POC setup

MNIST Handwritten text recognition using keras

### Architecture

- VPC

  - IGW
  - 2 subnets (1 private / 1 public)

- EC2

  - **TRAINMACHINE:** 

    - in public subnet

    - Open port 8888 for jupyter

    - ubuntu AMI, m5.xlarge

    - create venv / install requirements.txt

    - install jupyter notebook

    - add kernel for this venv

    - run 00-mnist-cnn.ipynb on created kernel

    - it will create model file: cnn-minst

      

  - **FRONTEND Server**

    - in public subnet

    - Open port 80 for web access

    - ubuntu AMI, t2.micro

    - install nginx

      ```
      sudo apt update
      sudo apt install nginx
      ```
  
- copy index.html and static folder in /var/www/html/
  
  - modify index.html with your BACKEND public IP.
    
  
  
  
- **BACKEND Server**
    - in private subnet
  - ubuntu AMI, t2.micro
    - route private subnet to NAT instance
    - allow inbound port 5000 from anywhere
    - create venv / install requirements.txt

    ```
  conda create -n backend
    conda activate backend
  conda install opencv
    pip install -r requirements.txt
    ```
  ```
  
  - copy cnn-minst / keras_flask.py
  - launch keras_flask.py
  
    ```bash
  python keras_flask.py
```
  

    
- USE

  <img src="webinterface.png" alt="webinterface" style="zoom:50%;" />

  

  <img src="backend_Flask_answer.png" alt="backend_Flask_answer" style="zoom:50%;" />

  

  

  

  - > **NAT INSTANCE**
  >
    > - in public subnet
  >
    > - amzn-ami-vpc-nat AMI, t2.micro
  >
    > - allow all inbound from local
  >
    > - do not forget to disable source/dest check
  >
  
