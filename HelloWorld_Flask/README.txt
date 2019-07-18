The test on this folder creates a Python-Flask "Hellow World" web app Docker container.

PREREQUISITES

This test runs on Docker Desktop for Windows.


INSTRUCTIONS

- Download the repository and once Docker Desktop is running, go to the folder where the files have been installed, for example C:\DockerTests\HelloWorld_Flask.

- On the command prompt, run the following command to create the docker image.

  docker build -t flask-tutorial:latest .

  A new image called flask-tutorial will be created. 

- Run the following command to run the container

  docker run -p 5000:5000 flask-tutorial

- In order to verify that the container is accepting request, open a browser and type the following address:

  http://localhost:5000

  A window showing "Hello World!" in the left upper corner should be shown.