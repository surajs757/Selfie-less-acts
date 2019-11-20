# selfie-less-acts
A containerized web application build using flask and docker

The web app uses a microservice architecture along with an orchestrator to ensure robust and efficient functioning of the servers.

## Installation

Docker must be installed on the server-system before the application can be run on it.
https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce


Flask module along with flask_cors must be installed to build the servers. Docker py is also used as a dokcer API with python
```
pip install flask
pip install flask_cors
pip install docker-py
```


## Execution

Each of the containers can be placed in separate servers to maintain microservice architecture.
For fault tolerance and scalability, the acts server is maintained by running on multiple containers which are increased or decreased depending on the need for scaling up or down.
To maintain persistant data among all running containers, the data contained in each container, ```/static``` is stored in a docker volume. Thus, the created volume should contain the contents of the ```static``` folder.

https://docs.docker.com/storage/volumes/


Build both the images by navigating to the folders 'actscontainer' and 'usercontainer' and running:
```
docker build .
```
After the image of the container is built, run the users container using:
```
docker run -p <req_port>:8000 <imageid> 
```
The image_id is displayed at the end of the build process.
The req_port corresponds to the port number where the application needs to listen at.

For the acts container:
```
docker run --name acts_0 -p <req_port>:8000 -v <volume_name>:/usr/bin/static <imageid> 
```
The path after the volume name corresponds to wherever the flask file is stored in the container. In this case, ```/usr/bin/static```.

Next the orchestrator needs to be run on the same server as the acts-container. By default, the orchestrator listens at port 80. This can be changed in the source code of orchestrator.py by changing the ```app.run()``` function's parameters.
Run the orchestrator using
```
python orchestrator.py
```

The orchestrator ensures fault tolerance by polling each container every second and in case of any faults, the container is immediately removed and a new one is started in its place.It also ensures scalability by increasing the number of containers running based on the number of requests made in the last two minutes. For every 20 extra requests a new container is added.

Ex: if 100 requests are made in the past 2 minutes, the number of containers are increased to 5. If only 3 requests are made in the subsequent two minutes, the number of containers are reduced back to 1.

Note:If the servers are cloud based, such as amazon ec2 instances, it would be ideal to use an aws load balancer to forward requests to the orchestrator on one instance and the acts container on the other one.
