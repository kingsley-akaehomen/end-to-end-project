DOCKERFILE INSTRUCTIONS AND EXPLANATIONS

'FROM'

 Purpose: Sets the base image for your Docker image.

 Examples: FROM python:3.10-slim, FROM ubuntu:22.04

 Explanation: Every Dockerfile starts with FROM like choosing the underlined operating system . It tells Docker which existing 
 image to build your image on top of.


'WORKDIR'

 Purpose: this instruction sets the working directory inside the container.

 Example: WORKDIR /app

 Explanation: All subsequent instructions (like RUN, ENTRYPOINT, COPY, and ADD etc.) will be executed in this directory. 

 
'RUN'

 Purpose: Executes commands in a new layer during image build and commits the result.

 Example: RUN pip install -r requirements.txt

 Explanation: Docker will read your command and build it into your image as a seperate image layer. 
 Useful for installing software or making system-level changes. 

'COPY'

 Purpose: Copies files or directories from your host machine into the container.

 Example: COPY . /app

 Explanation: It copies new files and directories from the source into the container's filesystem during build time. 

'CMD'

 Purpose: This sets the default command to run when the container starts based on this image.

 Example:  CMD ["python", "app.py"]

 Explanation: Each Dockerfile only has one CMD, and only the last CMD instance is respected when multiple exist.

'ENTRYPOINT'

 Purpose: Sets the main command to run, similar to CMD.

 Examples: ENTRYPOINT ["python"] , ENTRYPOINT ["fastapi"]

 Explanation: This sets the primary command your docker container will run everytime it starts. It specifys default executable.

'ENV'

 Purpose: Sets environment variables.

 Example:  ENV PORT=8080

 Explanation: The ENV sets the environment variables which are key configuration option that can dictate the behavioral pattern 
 of the application or software within the image.The ENV instruction allows for multiple <key>=<value> ... variables to be set
 at one time and these variables will persist when a container is run from the resulting image. You can view the values using - 
 docker inspect, and change them using - docker run --env <key>=<value>.


'EXPOSE'

 Purpose: Documents the port the app uses.

 Example:  EXPOSE 8080

 Explanation: This just describes which ports your application is listening on. Doesn’t publish the port—just a hint. 
 Use -p in ( docker run ) to actually expose.


'VOLUME'

 Purpose: Creates a mount point for a volume.

 Example:  VOLUME /data

 Explanation: This is used to persist data or share data between containers/host. The VOLUME instruction creates a mount point 
 with the specified name and marks it as holding externally mounted volumes from native host or other containers.


Layer caching and how Docker images are built:

-  Each Dockerfile instruction creates a layer.
-  Docker caches these layers to speed up rebuilds.
-  If a line changes, all lines after it are rebuilt.
-  Tip: Put less frequently changed lines (like pip install) early to leverage caching.

The difference between CMD and ENTRYPOINT in Docker:

CMD :- Think of it as a default suggestion.
       You can override it when you run the container.
       Used when you want to give a default command but allow flexibility.

ENTRYPOINT :- Think of it as a fixed command.
              You can’t override it easily—only pass extra arguments
              Used when you always want the container to run one specific program. 


Best Practices for writing clean, efficient Dockerfiles:-

Use small base images (e.g., alpine, slim) to reduce image size.
Use .dockerignore like .gitignore to exclude unnecessary files.
Use multi-stage builds to keep final images lean.
Pin versions of packages to avoid unexpected updates.
Avoid secrets in Dockerfiles (e.g., API keys).