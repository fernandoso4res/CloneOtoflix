from time import sleep
import pika, json
from config import *
# from mail import send_mail

def create_connection():
    connection = None
    cont = 0
    url = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/%2f'
    parameters = pika.URLParameters(url)
    sleep(35)
    while not connection:
        try:
            sleep(5)
            print('Tentando conectar ao rabbitmq pela URL:')
            print(url)
            cont += 1
            print('Tentativa:', cont)
            connection = pika.BlockingConnection(parameters)
        except:
            print("Erro ao conectar na tentativa:", cont)
            continue
    print('Conectado com sucesso na tentativa:', cont)
    return connection


def on_message(channel, method_frame, header_frame, body):
    # send_mail(json.loads(body))
    # channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == "__main__":
    try:
        connection = create_connection()
        channel = connection.channel()
        print('Iniciando consumo da fila:', QUEUE_NAME)
        channel.basic_consume(QUEUE_NAME, on_message)
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()