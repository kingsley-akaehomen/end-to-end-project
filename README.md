APP DESCRIPTION:
This is a simple Python applicatiom that displays the current date and time.

 This lightweight application's server can be launched with the command below on the terminal: 
  uvicorn time-api.py:app

 After the server is launched, execute a get request on the browser with the route:
  localhost:8000/ - Hello world display
  localhost:8000/time - current time display

 Copy dependencies to requirements.txt with the command below:
  pip3 freeze > requirements.txt

 Start the server with the comment
  uvicorn time-display:app

 Run the command to build the docker image
  docker build -t time-api . (the . means find a docker file in the root directory)

 Run the command below to create the container
  docker run --rm -it -p 8000:8000 time-api bash (defined port 8000)

 Start sever with the command inside the docker container
  uvicorn time-api:app --host=0.0.0.0   (host=0.0.0.0 means default to outside of containers)

 Use the docker 'compose command' below to build the image, start the container map the container pots to host ports
  docker compose up