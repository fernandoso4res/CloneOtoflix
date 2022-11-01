from os import getenv

QUEUE_NAME = 'notification'
RABBITMQ_USER = getenv('RABBITMQ_USER')
RABBITMQ_PASS = getenv('RABBITMQ_PASS')
RABBITMQ_HOST = getenv('RABBITMQ_HOST')
RABBITMQ_PORT = getenv('RABBITMQ_PORT')