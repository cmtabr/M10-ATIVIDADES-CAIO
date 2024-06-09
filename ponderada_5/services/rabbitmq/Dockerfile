FROM rabbitmq:3.13-management

ENV RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS="-rabbitmq_management load_definitions \"/etc/rabbitmq/definitions.json\""

ADD --chown=rabbitmq definitions.json /etc/rabbitmq/
ADD --chown=rabbitmq rabbitmq.conf /etc/rabbitmq/
ADD --chown=rabbitmq  ./certs/ /etc/rabbitmq/

RUN rabbitmq-plugins enable rabbitmq_mqtt rabbitmq_top