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
    'CLI_DESCRIPTION': "CLI for a simple Kafka consumer.",
    'CLI_PROG': "consumer",

    # Logging
    'STANDARD_LOG_LEVEL': logging.ERROR,
    'VERBOSE_LOG_LEVEL': logging.INFO,

    # Default values for command-line arguments
    'ARG_BOOTSTRAP': os.environ.get('CONSUMER_BOOTSTRAP', "localhost:9092"),
    'ARG_TOPIC': os.environ.get('CONSUMER_TOPIC', 'wav-test'),

    # Kafka connection configuration
    'KAFKA_group.id': 'wav-consumer',
    'KAFKA_auto.offset.reset': 'earliest'
}