APP DESCRIPTION:
This is a simple Python applicatiom that displays the current date and time.

# This lightweight application's server can be launched with the command below on the terminal: 
  uvicorn time-api.py:app

# After the server is launched, execute a get request on the browser with the route:
  localhost:8000/ - Hello world display
  localhost:8000/time - current time display

# copy dependencies to requirements.txt with the command below:
  pip3 freeze > requirements.txt

# start the server with the comment
uvicorn time-display:app

# run the command to build the docker image
docker build -t time-api . 

# run the command below to create the container
docker run --rm -it -p 8000:8000 time-api bash

# start sever with the command inside the docker container
uvicorn time-api:app --host=0.0.0.0   