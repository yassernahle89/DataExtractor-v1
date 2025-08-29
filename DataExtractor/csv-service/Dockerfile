FROM python:3.11-slim

ENV BOOTSTRAP_SERVERS=redpanda-0.uaenorth.cloudapp.azure.com:9094,redpanda-1.uaenorth.cloudapp.azure.com:9094,redpanda-2.uaenorth.cloudapp.azure.com:9094


# Install git and other dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

WORKDIR /app
EXPOSE 8021

COPY . /app

# Install dependencies including the shared_lib from GitHub
RUN pip install --no-cache-dir fastapi uvicorn kafka-python confluent_kafka dotenv \
    && pip install --no-cache-dir "git+https://github.com/yassernahle89/shared_Lib.git#egg=shared_lib"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8021"]
