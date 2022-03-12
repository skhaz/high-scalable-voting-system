## Architecture

This project is a small but highly scalable voting system based on Big Brother Brasil's voting system.

At the front, a load balancer will distribute the load across N instances of the backend container in a production environment.

The backend exposes an API to vote. It just put the unique identifier of the request onto the RabbitMQ queue.

Another process, called worker, will be listening on the same RabbitMQ queue. When a new message arrives, it just increments the key, the UID on Redis.

Everything is horizontally scalable.

### Voting

Vote for a person using its UID (unique id), for example UID 1

``` shell
http localhost:3000/vote uid=1
```

Get the stats of an UID

``` shell
http GET localhost:3000/stats/1
```

Reset all counters

``` shell
http POST localhost:3000/reset
```

All examples are using [HTTPie](https://httpie.io/).

### What is missing?

Kubernetes. I will update this repo soon with it.

### Diagram

![diagram](../docs/diagram.png?raw=true)
