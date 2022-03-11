from diagrams import Diagram
from diagrams.onprem.container import Docker
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ

with Diagram("diagram", show=False, direction="TB"):
    (
        Nginx("load balancer")
        >> [Docker("backend"), Docker("backend"), Docker("backend")]
        >> RabbitMQ("rabbitmq")
        >> [Docker("worker"), Docker("worker"), Docker("worker")]
        >> Redis("redis")
    )
