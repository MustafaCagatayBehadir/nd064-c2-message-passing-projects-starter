import time
import json
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

from kafka import KafkaProducer


TOPIC_NAME = 'locations-topic'
KAFKA_SERVER = 'kafka-service:9092'


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Get(self, request, context):
        return

    def Create(self, request, context):
        from app.udaconnect.services import LocationService
        location = {
            "person_id": request.person_id,
            "latitude":  request.latitude,
            "longitude": request.longitude
        }
        print(location)
        producer = self.kafka_producer()
        producer.send("locations-topic", location)
        producer.flush()
        return location_pb2.LocationMessage(**location)

    @staticmethod
    def kafka_producer():
        # Set up a Kafka producer
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        )
        return producer


if __name__ == "__main__":
    # Initialize gRPC server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    location_pb2_grpc.add_LocationServiceServicer_to_server(
        LocationServicer(), server)

    print("Server starting on port 5005...")
    server.add_insecure_port("[::]:5005")
    server.start()
    # Keep thread alive
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
