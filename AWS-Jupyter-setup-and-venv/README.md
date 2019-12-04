# Jupyter / Python / Venv setup



## Initital setup

- Create EC2 instance using AMI Ubuntu 18.04 Server, publicly accessible
- in Security Group: open port 8888 from anywhere
- connect trough ssh



## Install / Check Python and pip

- Check if python3 is installed

  ```bash
  python3 --version
  ```

- **1st thing** always: update

  ```bash
  sudo apt-get install -y
  ```

- install pip (same version as python pip3)

  ```bash
  sudo apt-get install python3-pip -y
  ```

- Check pip3 version

  ```bash
  pip3 --version
  ```



## Install Jupyter

- install Jupyter

  ```bash
  sudo pip3 install jupyter
  ```

- Launch Jupyter notebook (default binding is 127.0.0.1:8888)

  ```bash
  jupyter notebook --ip=0.0.0.0
  ```

- Check running Jupyter notebooks

  ```bash
  jupyter notebook list
  ```

- Stop running Jupyter notebook

  ```bash
  jupyter notebook stop 8888
  ```

- Run with **nohup** (no more link to terminal - stay alive even if terminal is closed)

  ```bash
  nohup jupyter notebook --ip=0.0.0.0 &
  ```

- Get the token

  ```bash
  cat nohup.out
  ```



## Install / Create virtual environments (using conda)

- Install mini-conda

  ```
  wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
  sh Miniconda3-latest-Linux-x86_64.sh
  ```

  *Follow instructions / restart terminal*

- Create virtual environment with python 3.6

  ```bash
  conda create -n <venv_name> python=3.6
  ```

- activate virtual environment

  ```bash
  conda activate <venv_name>
  ```

- Deactivate virtual environment

  ```bash
  conda deactivate
  ```

- List existing environments

  ```bash
  conda env list  
  ```

- Remove virtual environment (deactivate first)

  ```bash
  conda env remove --name <venv_name>
  ```



## Add kernel to Jupyter

- In your virtual environment, Install in ipykernel (if needed)

  ```bash
  conda install ipykernel
  or 
  pip install ipykernel
  NOT --> pip3 install ipykernel !! (check warning below)
  ```

- create linked kernel in Jupyter

  ```bash
  python3 -m ipykernel install --user --name=<name_in_jupyter>
  ```

- list kernel installed

  ```bash
  jupyter kernelspec list
  ```

- remove kernel

  ```bash
  jupyter kernelspec uninstall <name_in_jupyter>
  ```



## WARNING !!!

In Conda virtual environment use pip not pip3 !!!

<img src="pip_vs_pip3.png" alt="pip_vs_pip3" style="zoom:50%;" />

## Get virtual environment installed packages

- get the list of installed packages in current virtual environment and save it to file

  ```bash
  pip freeze > requirements.txt
  ```

- install packages from requirements.txt in another virtual environment

  ```bash
  pip install -r requirements.txt
  ```



