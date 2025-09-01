from fastapi import FastAPI
from shared_lib.kafka_consumer import KafkaConsumerService
from shared_lib.mongo_connector import MongoWriter
from dotenv import load_dotenv
import os
import json

app = FastAPI()

load_dotenv()
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
mongodb_url=os.getenv("MONGODB_URL")


# Globals
mongo_writer: MongoWriter = None
consumer: KafkaConsumerService = None

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
    if mongo_writer is not None:
        mongo_writer.insert(msg)

@app.on_event("startup")
def start_kafka_consumer():
    global mongo_writer, consumer

    # setup Mongo
    mongo_writer = MongoWriter(
        uri=mongodb_url,
        db="Redpanda",
        collection="messages"
    )
    mongo_writer.connect()

    consumer = KafkaConsumerService(
        topic="web-scraping",
        bootstrap_servers=bootstrap_servers,
        group_id="Data-Extractor-web-scraping",
        callback=handle_kafka_message,
    )
    consumer.start()


@app.on_event("shutdown")
def stop_kafka_consumer():
    global mongo_writer, consumer

    if consumer:
        consumer.stop()
    if mongo_writer:
        mongo_writer.close()