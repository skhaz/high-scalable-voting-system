import os
from urllib.parse import urlparse

from pika.adapters import SelectConnection
from pika.connection import ConnectionParameters
from pika.credentials import PlainCredentials
from redis import ConnectionPool, StrictRedis

channel = None

redis = StrictRedis(connection_pool=ConnectionPool.from_url(os.environ["REDIS_DSN"]))


def on_connected(connection):
    connection.channel(on_open_callback=on_channel_open)


def on_channel_open(new_channel):
    global channel
    channel = new_channel
    channel.queue_declare(
        queue="votes",
        durable=True,
        exclusive=False,
        auto_delete=False,
        callback=on_queue_declared,
    )


def on_queue_declared(frame):
    channel.basic_consume("votes", handle_delivery)


def handle_delivery(channel, method, header, body):
    redis.incr(body.decode("utf-8"))


fragments = urlparse(os.environ["AMQP_DSN"])

credentials = PlainCredentials(fragments.username, fragments.password)

connection = SelectConnection(
    ConnectionParameters(
        fragments.hostname,
        fragments.port,
        fragments.path,
        credentials,
    ),
    on_open_callback=on_connected,
)


def main():
    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()


if __name__ == "__main__":
    main()
