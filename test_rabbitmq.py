import pika
from os import environ


if __name__ == "__main__":
    username = "guest"
    password = "guest"
    host = environ.get("RABBITMQ_HOST")
    vhost = "/"
    
    print(f"RABBITMQ_HOST: {host}")

    credentials = pika.credentials.PlainCredentials(username, password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        virtual_host=vhost,
        credentials=credentials))

    channel = connection.channel()
    print(channel)
    # method_frame, header_frame, body = channel.basic_get("test")
    # if method_frame:
    #     print(method_frame, header_frame, body)
    #     channel.basic_ack(method_frame.delivery_tag)
    # else:
    #     print("No message returned")