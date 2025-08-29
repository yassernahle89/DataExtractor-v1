from fastapi import FastAPI
from shared_lib.kafka_consumer import KafkaConsumerService
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")

def handle_kafka_message(msg: dict):
    print("Processing message:", msg)

@app.on_event("startup")
def start_kafka_consumer():
    consumer = KafkaConsumerService(
        topic="web-scraping",
        bootstrap_servers=bootstrap_servers,
        group_id="Data-Extractor",
        callback=handle_kafka_message,
    )
    consumer.start()
