import asyncio
import logging
import aio_pika
from aio_pika import Message, connect_robust
from aio_pika.abc import AbstractIncomingMessage
from os import environ


async def simple_consumer() -> None:
    username = "guest"
    password = "guest"
    host = environ.get("RABBITMQ_HOST")
    # vhost = "/"
    
    print(f"RABBITMQ_HOST: {host}")
    
    queue_name = "test_queue_name"
    exchange_name = "amq.topic"
    routing_key = "test_routing_key"

    logging.basicConfig(level=logging.DEBUG)
    connection = await aio_pika.connect_robust(
        f"amqp://{username}:{password}@{host}/",
    )

    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Will take no more than 10 messages in advance
        await channel.set_qos(prefetch_count=10)

        # Declaring queue
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

                    if queue.name in message.body.decode():
                        break


async def simple_consumer() -> None:
    username = "guest"
    password = "guest"
    host = environ.get("RABBITMQ_HOST")
    # vhost = "/"
    
    print(f"RABBITMQ_HOST: {host}")
    
    queue_name = "test_queue_name"
    exchange_name = "amq.topic"
    routing_key = "test_routing_key"

    connection = await aio_pika.connect_robust(
        f"amqp://{username}:{password}@{host}/",
    )

    async with connection:
        routing_key = "test_queue"

        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=f"Hello {routing_key}".encode()),
            routing_key=routing_key,
        )

async def send_and_get() -> None:
    username = "guest"
    password = "guest"
    host = environ.get("RABBITMQ_HOST")
    # vhost = "/"
    
    print(f"RABBITMQ_HOST: {host}")
    
    # queue_name = "test_queue_name"
    exchange_name = "amq.topic"
    # routing_key = "test_routing_key"

    connection = await aio_pika.connect_robust(
        f"amqp://{username}:{password}@{host}/",
    )

    queue_name = "test_queue"
    routing_key = "test_queue"

    # Creating channel
    channel = await connection.channel()
    
    print(channel)

    # Declaring exchange
    exchange = await channel.declare_exchange("direct", auto_delete=True)

    # Declaring queue
    queue = await channel.declare_queue(queue_name, auto_delete=True)

    # Binding queue
    await queue.bind(exchange, routing_key)

    await exchange.publish(
        Message(
            bytes("Hello", "utf-8"),
            content_type="text/plain",
            headers={"foo": "bar"},
        ),
        routing_key,
    )

    # Receiving message
    if incoming_message := await queue.get(timeout=5, fail=False):
        # Confirm message
        print(f"incoming_message: {incoming_message}")
        await incoming_message.ack()
    else:
        print("Queue empty")

    await queue.unbind(exchange, routing_key)
    await queue.delete()
    await connection.close()


if __name__ == "__main__":
    # asyncio.run(simple_consumer())
    asyncio.run(send_and_get())
