import json
from kafka import KafkaConsumer

# Define Kafka consumer function


def consume_persons_topic():
    from app.udaconnect import PersonService
    from app import create_app

    TOPIC_NAME = 'persons-topic'
    KAFKA_SERVER = 'kafka-service:9092'
    CONSUMER_GROUP = "persons-consumers"
    consumer = KafkaConsumer(
        client_id="client-persons",
        group_id=CONSUMER_GROUP,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    consumer.subscribe(topics=[TOPIC_NAME])

    for message in consumer:
        print(message.value)
        _app = create_app()
        with _app.app_context():
            PersonService.create(message.value)


if __name__ == '__main__':
    while True:
        consume_persons_topic()
