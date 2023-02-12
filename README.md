# BackendCodingTest





Running application using Docker container (preferred):

PREREQUISITES:

1. System should have Docker installed and running(important!). I use Docker desktop, but the docker-cli can also be used. 
Commands for installing docker-cli:
sudo apt-get update  
sudo apt-get install docker-ce docker-ce-cli containerd.io 

2. Port 8000 on machine should be free. 

STEPS:

1. Clone this git repository
2. Build the docker container by running the following command:
    docker build . -t message-app
3. Run the docker container by running the following command:
   docker run -dp 8000:8000 -it message-app  
4. Navigate to localhost:8000 and begin using application


Steps to run application locally without using Docker:

1. Clone git repository
2. Run the following command:
  python3 -m venv virtualenvironment 
3. Activate the virtual environment by running the following command:
  source virtualenvironment/bin/activate 
4. Install dependencies by running:
  pip install -r requirements.txt
5. Start application by running the command:
  python manage.py runserver

