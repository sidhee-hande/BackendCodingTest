# BackendCodingTest

**Running application using Docker container (preferred):**

**PREREQUISITES:**

1. System should have Docker installed and running(important!). I use Docker desktop, but the docker-cli can also be used. 
Commands for installing docker-cli:
sudo apt-get update  
sudo apt-get install docker-ce docker-ce-cli containerd.io 

2. Port 8000 on machine should be free. 

**STEPS:**

1. Clone this git repository
2. Build the docker container by running the following command:
    docker build . -t message-app
3. Run the docker container by running the following command:
   docker run -dp 8000:8000 -it message-app  
4. Navigate to localhost:8000 and begin using application


 &nbsp;



**Running application locally without using Docker:**

**PREREQUISITES:**

1. System should have python3 and pip3 installed. 

**STEPS:**
1. Clone git repository
2. Run the following command:
  python3 -m venv virtualenvironment 
3. Activate the virtual environment by running the following command:
  source virtualenvironment/bin/activate 
4. Install dependencies by running:
  pip install -r requirements.txt
5. Start application by running the command:
  python manage.py runserver


 &nbsp;
 
 **Information regarding Database files:**
 The project uses an sqlite3 database which has been populated with 2 users and 3 messages as a sample.
 
 **USER CREDENTIALS TO TEST PROJECT:**
   &nbsp;
   
   **username:**  sidheehande  **password:** a1d2m3i4n5 
   &nbsp;
   
   **username:** constructionbevy **password:** a1d2m3i4n5

&nbsp;

**FUTURE SCOPE:**
1. The messages can be encrypted for extra protection.
2. Adding a "restore deleted messages" option which will be easy to implement since the message is not actually deleted from the database, rather its status is marked as deleted, and it is not displayed in lists for that specific user.
3. Improving frontend by using VueJS, and adding a search option for particular sender/recipient in the Inbox and Sentbox pages.
4. Extending to use a MySQL server and building separate containers for it in Docker.


