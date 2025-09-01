from fastapi import FastAPI
from shared_lib.kafka_consumer import KafkaConsumerService
from dotenv import load_dotenv
import os
import json 

app = FastAPI()

load_dotenv()
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")

# Common handler for both Kafka and API
def print_if_json(msg):
    if isinstance(msg, dict):
        # Already parsed JSON
        print(msg)
    elif isinstance(msg, str):
        try:
            parsed = json.loads(msg)
            print(parsed)  # dict-style print: {"user": "yasser", "message": "hello world"}
        except json.JSONDecodeError:
            print("Received non-JSON string:", msg)
    else:
        print("Received unknown type:", msg)

# Handle Kafka messages
def handle_kafka_message(msg: dict):
    print_if_json(msg)

@app.on_event("startup")
def start_kafka_consumer():
    consumer = KafkaConsumerService(
        topic="pptx",
        bootstrap_servers=bootstrap_servers,
        group_id="Data-Extractor-pptx",
        callback=handle_kafka_message,
    )
    consumer.start()
