from fastapi import FastAPI
from shared_lib.kafka_consumer import KafkaConsumerService
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")

# Common handler for both Kafka and API
def print_if_json(msg):
    if isinstance(msg, dict):
        print(msg)  # prints like {"user": "yasser", "message": "hello world"}
    else:
        print("Received non-JSON message:", msg)

# Handle Kafka messages
def handle_kafka_message(msg: dict):
    print_if_json(msg)

@app.on_event("startup")
def start_kafka_consumer():
    consumer = KafkaConsumerService(
        topic="pptx",
        bootstrap_servers=bootstrap_servers,
        group_id="Data-Extractor",
        callback=handle_kafka_message,
    )
    consumer.start()
