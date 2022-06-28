import pika
from os import environ
import platform
    
def main():
    print(f"Python version: {platform.python_version()}")

    username = "guest"
    password = "guest"
    host = environ.get("RABBITMQ_HOST")
    vhost = "/"
    
    print(f"RABBITMQ_HOST: {host}")
    
    queue_name = "test_queue_name"
    exchange_name = "amq.topic"
    routing_key = "test_routing_key"
    
    credentials = pika.credentials.PlainCredentials(username, password)
    publish(host, vhost, credentials, exchange_name, routing_key, queue_name)
    consume(host, vhost, credentials, exchange_name, routing_key, queue_name)

    
def publish(host, vhost, credentials, exchange_name, routing_key, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        virtual_host=vhost,
        credentials=credentials))
    channel = connection.channel()
    
    print(f"connection: {connection}")
    print(f"channel: {channel}")

    channel.publish(
        exchange=exchange_name, routing_key=routing_key, body="message body value"
    )


def consume(host, vhost, credentials, exchange_name, routing_key, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        virtual_host=vhost,
        credentials=credentials))
    channel = connection.channel()
    
    print(f"connection: {connection}")
    print(f"channel: {channel}")
    
    try:
        channel.queue_declare(queue=queue_name, passive=True)
    except pika.exceptions.ChannelClosed:
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
    channel.queue_bind(queue_name, exchange_name, routing_key=routing_key)

    method_frame, header_frame, body = channel.basic_get(queue_name)
    if method_frame:
        print("received message")
        print(method_frame, header_frame, body)
        channel.basic_ack(method_frame.delivery_tag)
    else:
        print("No message returned")
        
    connection.close()


if __name__ == "__main__":
    main()
