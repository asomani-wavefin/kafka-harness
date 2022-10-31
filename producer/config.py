# config.py
"""Global configuration settings.

Loads all settings, permitting override from environment variables and .env file. Access 
these settings from any module using the settings dict.

"""

from dotenv import load_dotenv
import logging
import os

# Load environment variables from .env
load_dotenv()

settings = {
    # CLI configuration
    'CLI_DESCRIPTION': "CLI for a simply Kafka producer.",
    'CLI_PROG': "producer",

    # Logging
    'STANDARD_LOG_LEVEL': logging.ERROR,
    'VERBOSE_LOG_LEVEL': logging.INFO,

    # Default values for command-line arguments
    'ARG_BOOTSTRAP': os.environ.get('PRODUCER_BOOTSTRAP', "localhost:9092"),
    'ARG_COUNT': os.environ.get('PRODUCER_COUNT', 5),
    'ARG_SLEEP': os.environ.get('PRODUCER_SLEEP', 3),
    'ARG_TOPIC': os.environ.get('PRODUCER_TOPIC', 'wav-test'),

    # Kafka connection configuration
    'KAFKA_delivery.timeout.ms': 30000,                   # 30 seconds
    'KAFKA_request.timeout.ms': 10000,                    # 10 seconds
    'KAFKA_socket.connection.setup.timeout.ms': 10000,    # 10 seconds
    'KAFKA_transaction.timeout.ms': 30000                 # 30 seconds

}
