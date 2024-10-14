# Welcome to Crypto AES!

Crypto AES is a web application that encrypts and decrypts messages using AES with a key size of 256 bits. The application is built using the Python Django framework.


# Run
To run the project locally, you have two options.

## Option 1: Docker
Requirements:
 - [Docker](https://www.docker.com/)
 - [Docker Compose](https://docs.docker.com/compose/)

by using **docker-compose.yml** file.

    docker-compose up
Access the app on **http://127.0.0.1:8000**
## Option 2: Django development server
Requirements:
 - [python 3](https://www.python.org/downloads/)
 - [pip](https://pypi.org/project/pip/)

Run the following commands

    pip install -r requirements.txt
    python .\app\manage.py runserver
Access the app on **http://127.0.0.1:8000**
 


