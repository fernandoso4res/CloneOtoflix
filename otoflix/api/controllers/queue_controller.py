from ext.queue import publish
import json


def send_to_queue(exchange, routing_key, message: str):
    if not isinstance(message, str):
        raise TypeError
    publish(exchange, routing_key, message)


def send_email(recipients, email_type, **kwargs):
    exchange = 'exchange_email'
    routing_key = 'routing_key_email'
    message = {
        'recipients': recipients,
        'email_type': email_type,
        'kwargs':kwargs
    }
    message = json.dumps(message)
    send_to_queue(exchange, routing_key, message)

