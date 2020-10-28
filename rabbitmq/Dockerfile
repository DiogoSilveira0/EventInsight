FROM rabbitmq:3.8

ENV RABBITMQ_DEFAULT_USER user
ENV RABBITMQ_DEFAULT_PASS user

RUN rabbitmq-plugins enable rabbitmq_management
RUN rabbitmq-plugins enable rabbitmq_mqtt

EXPOSE 15672
EXPOSE 5672
EXPOSE 1883