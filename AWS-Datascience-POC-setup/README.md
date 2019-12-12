# AWS DataScience POC setup

MNIST Handwritten text recognition using Keras / TensorFlow

### Architecture

- VPC

  - IGW
  - 2 subnets (1 private / 1 public)

- EC2

  - **TRAINMACHINE:** 

    - in public subnet

      - Open port 8888 for Jupyter
      - ubuntu AMI, m5.xlarge
	  
	- Install Miniconda
  
      ```bash
      wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
	  sh Miniconda3-latest-Linux-x86_64.sh
      ```
  
	- Files to be copied from [TRAINMACHINE](TrainMachine/) folder
	
    - create virtual environment / install requirements.txt
  
    - install jupyter notebook
  
    - add kernel for this virtual environment
  
    - run 00-mnist-cnn.ipynb on created kernel
  
    - it will create model file: cnn-minst
  
    
  
  - **FRONTEND Server**
  
    - in public subnet
  
      - Open port 80 for web access
      - ubuntu AMI, t2.micro
  
    - install nginx
  
      ```bash
      sudo apt update
      sudo apt install nginx
      ```
    
	- Files to be copied from [FRONTEND](FrontEnd/) folder
		
    - copy index.html and static folder in /var/www/html/
		
    - modify index.html with your BACKEND public IP.
  
  
  
  - **BACKEND Server**
    
    - in public subnet
    
      - ubuntu AMI, t2.micro
      - open port 5000
    
    - Install Miniconda
    
      ```bash
      wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
      sh Miniconda3-latest-Linux-x86_64.sh
      ```
	  
    - Files to be copied from [BACKEND](BackEnd/) folder
		
    - create virtual environment / install requirements.txt
    
      ```bash
      conda create -n backend
      conda activate backend
      conda install opencv
      pip install -r requirements.txt
      ```
    
    - copy cnn-minst / keras_flask.py
		
    - launch keras_flask.py
    
      ```
      python keras_flask.py
      ```
  
- USE

  <img src="webinterface.png" alt="webinterface" style="zoom:50%;" />

  

  <img src="backend_Flask_answer.png" alt="backend_Flask_answer" style="zoom:50%;" />

  

