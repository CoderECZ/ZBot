import pika
import 

def callback(ch, method, properties, body):
    '''Callback function for incoming messages.'''
    
    print(f"Received message: {body}")

# Establish connection to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the same exchange name as in the Rust application
channel.exchange_declare(exchange='webhooks', exchange_type='direct')

# Declare a queue
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Bind the queue to the exchange with a routing key
channel.queue_bind(exchange='webhooks', queue=queue_name, routing_key='webhook.routing_key')

# Set up the callback function for incoming messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

# Start consuming messages
print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
