from config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS
import pika



def create_connection():
      parameters = pika.URLParameters(f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/%2f')
      return pika.BlockingConnection(parameters)

def publish(exchange, routing_key, message):
      connection = create_connection()
      connection.channel().basic_publish(exchange=exchange, routing_key=routing_key, body=message)
      connection.close()