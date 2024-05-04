This is the tutorial for the project. It will guide you through the project and help you understand the code and the
project structure.

## Table of Contents

1. [Client](#client)
2. [Service](#service)
3. [Server](#server)
4. [Sample Test](#test)

## Client

This is the client side of the project.

The `Client` class has three methods:

1. `__init__`: This method initializes the client socket and connects to the server.
2. `send`: This method sends a message to the server and receives a response.
3. `disconnect`: This method closes the socket.

for running the client, you can use the following command:

```bash
python client.py # default values
```

OR

```bash
python client.py --requests_per_client 1000 --client_count 1 --balancerPort 8080 --balancerIp localhost
```

You can also pass the following arguments to the client:

- `requests_per_client`: The number of requests each client will send to the server.
- `client_count`: The number of clients that will be created.
- `balancerPort`: The port number of the load balancer.
- `balancerIp`: The IP address of the load balancer.

## Service

This is a sample server which gets a number and returns `It It’s instance number <i>`

This file starts a server on a random port or the port specified in the command line arguments.
The server listens for incoming connections and sends a response to the client.

for running the service, you can use the following command:

```bash
python service.py # default values
```

OR

```bash
python service.py -p 9090
```

You can specify the port number of the server using the `-p` argument.

## Server

This is the load balancer server.
It listens for incoming connections from clients and forwards them to the services.
The server uses a round-robin algorithm to distribute the requests among the services.

The `Server` class is used to connect to the services and send messages to them. There are two methods in the class:

1. `check_connection`: This method checks if the server is available.
2. `send`: This method sends a message to the service and receives a response.

There is a scheduler that checks the health of the servers every `refreshRate` seconds.
If a server is down, the scheduler will remove it from the list of servers.
If the server comes back up, the scheduler will add it back to the list of servers.

for running the server, you can use the following command:

```bash
python server.py # default values
```

OR

```bash 
python server.py -p 8080 -refreshRate 60
```
You can specify the port number of the server using the `-p` argument.
You can specify the refresh rate of the servers' health check using the `-refreshRate` argument. It is the time in seconds.

Also, you can use the config in json format,
but you have to comment the commented `initialize_servers()` and uncomment the old `initialize_servers()`.


## Test

A sample test: Test the client and server.
These lines should run on separate terminals with the same order.
```bash
echo -e "localhost 8090\nlocalhost 8091\nlocalhost 8092\nlocalhost 8093" > config.txt
python service.py -p 8090
python service.py -p 8091
python service.py -p 8092
python service.py -p 8093
python server.py -p 8080  > load_balancer_output.txt &
python client.py --requests_per_client 1000 --client_count 1 --balancerPort 8080 --balancerIp localhost
```