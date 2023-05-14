import json
from kafka import KafkaConsumer

# Define Kafka consumer function

TOPIC_NAME = 'locations-topic'
KAFKA_SERVER = 'kafka-service:9092'

def consume_persons_topic():
    from app.udaconnect import LocationService
    from app import create_app
    
    CONSUMER_GROUP = "locations-consumers"
    consumer = KafkaConsumer(
        client_id="client-locations",
        group_id=CONSUMER_GROUP,
        bootstrap_servers=KAFKA_SERVER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    consumer.subscribe(topics=[TOPIC_NAME])

    for message in consumer:
        print(message.value)
        _app = create_app()
        with _app.app_context():
            LocationService.create(message.value)


if __name__ == '__main__':
    while True:
        consume_persons_topic()
