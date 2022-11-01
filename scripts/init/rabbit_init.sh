#!/bin/sh

( rabbitmqctl wait --timeout 50 /var/lib/rabbitmq/mnesia/rabbitmq ; \
rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASS 2>/dev/null ; \
rabbitmqctl set_user_tags $RABBITMQ_USER administrator ; \
rabbitmqctl set_permissions -p / $RABBITMQ_USER  ".*" ".*" ".*" ; \
rabbitmqadmin --username=$RABBITMQ_USER --password=$RABBITMQ_PASS declare exchange --vhost=/ name=exchange_email type=direct ; \
rabbitmqadmin --username=$RABBITMQ_USER --password=$RABBITMQ_PASS declare queue --vhost=/ name=queue_email durable=true ; \
rabbitmqadmin --username=$RABBITMQ_USER --password=$RABBITMQ_PASS --vhost=/ declare binding source=exchange_email destination_type=queue destination=queue_email routing_key=routing_key_email
) & rabbitmq-server $@