import pika
from os import environ

    
def main()
    username = "guest"
    password = "guest"
    host = environ.get("RABBITMQ_HOST")
    vhost = "/"
    
    print(f"RABBITMQ_HOST: {host}")
    
    credentials = pika.credentials.PlainCredentials(username, password)
    publish(credentials, host, vhost)
    consume(credentials, host, vhost)
    
def publish(credentials, host, vhost):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        virtual_host=vhost,
        credentials=credentials))
    channel = connection.channel()

    channel.basic_publish(
        'test_exchange',
        'test_routing_key',
        'message body value',
        pika.BasicProperties(content_type='text/plain',
        delivery_mode=pika.DeliveryMode.Transient))
    connection.close()

def consume(credentials, host, vhost):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        virtual_host=vhost,
        credentials=credentials))
    channel = connection.channel()
    print(channel)
    method_frame, header_frame, body = channel.basic_get("test")
    if method_frame:
        print(method_frame, header_frame, body)
        channel.basic_ack(method_frame.delivery_tag)
    else:
        print("No message returned")
    
    connection.close()

if __name__ == "__main__":
    main()
