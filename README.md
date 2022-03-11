## Architecture

Based on Big Brother Brasil's voting system I made this small but high scalable voting system.

In a production environment, a load balancer will distribute the load across N instances of the backend container.

The backend just exposes an API to vote, when a new vote is sent using POST, the backend will be sent a message to a queue on RabbitMQ and returns an HTTP 202 with a JSON.

Another process, called worker will be listening on the same RabbitMQ's queue, when a new message arrives, it just increments the key, which is the UID on Redis.

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
