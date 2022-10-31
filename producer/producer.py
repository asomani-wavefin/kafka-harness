# producer.py
"""Primary module for the producer package

Parses command line arguments and calls command-related functions.

Available functions:
- main: Main execution path. Parses the command line and delegates accordingly.

"""

__version__ = "0.1.0"

from confluent_kafka import KafkaException, Producer
from faker import Faker
import argparse
import json
import logging
import time

# Local imports
from .config import settings


# CLI_DESCRIPTION = settings.get('CLI_DESCRIPTION')
# CLI_PROG = settings.get('CLI_PROG')
# STANDARD_LOG_LEVEL = settings.get('STANDARD_LOG_LEVEL') 
# VERBOSE_LOG_LEVEL = settings.get('VERBOSE_LOG_LEVEL')

def main():
    """Main execution path. Parses the command line and delegates.
    """

    # Supress visibility of logger output
    logging.basicConfig(level=settings.get('STANDARD_LOG_LEVEL'))
    logger = logging.getLogger()

    # Set up argparse
    parser = argparse.ArgumentParser(description=settings.get('CLI_DESCRIPTION'), prog=settings.get('CLI_PROG'))
    parser.add_argument('--verbose', action="store_true", help="make the output verbose")
    parser.add_argument('-v', '--version', action="version", help="print the version of this software",
        version='{prog} version {ver}'.format(prog=settings.get('CLI_PROG'), ver=__version__))

    # Producer variables
    parser.add_argument('--bootstrap', action="store", type=ascii, default=settings.get('ARG_BOOTSTRAP'), help="comma-separated list for bootstrap.servers")
    parser.add_argument('--count', action="store", type=int, default=settings.get('ARG_COUNT'), help="number of messages to generate")
    parser.add_argument('--sleep', action="store", type=int, default=settings.get('ARG_SLEEP'), help="interval between message sends in seconds")
    parser.add_argument('--topic', action="store", type=ascii, default=settings.get('ARG_TOPIC'), help="topic on which messages will be sent")

    # Parse the command line and call the command
    try:
        args = parser.parse_args()

        # verbose option increases the logger visibility
        if args.verbose:
            logger.setLevel(settings.get('VERBOSE_LOG_LEVEL'))
            print("output mode set to VERBOSE\n")
        
        push_messages(
            args.bootstrap.strip("\'"), 
            args.count, 
            args.topic.strip("\'"), 
            args.sleep, 
            receipt_callback=cb_receipt)

    except:
        print("An error occured")
        exit(1)

    finally:
        print("")

    exit(0)

def init_producer(bootstrap_servers='') -> Producer:
    """Returns an initialized Kafka Producer connected to the specified broker.
    """

    logger = logging.getLogger()
    logger.info('Initiating Kafka Producer...')

    # Instantiate a Producer object.
    try:
        p = Producer(
            {'bootstrap.servers': bootstrap_servers})
        if p is None:
            logger.critical('Failed to initiate Kafka Producer!')
            return None
    except KafkaException as e:
        logger.exception(e)
        return None

    logger.info('Kafka Producer successfully initiated.')
    return p


def generate_message() -> str:
    """Generate a single fake json message. 
    """

    # use Faker to generate dummy message data
    fake = Faker()
    if fake is None:
        return '{}'

    # data structure of the json message
    data = {
        'user_id': fake.random_int(min=100000, max=999999),
        'user_name': fake.name(),
        'user_address': {
            'street': fake.street_address(),
            'city': fake.city(),
            'country': fake.country_code(),
        },
        'signup_at': str(fake.date_time_this_month()) }

    # return the message as a json string
    try:
        msg = json.dumps(data)
        return msg
    except:
        return '{}'

    
def cb_receipt(err, msg):
    """Receipt callback function for pushed messages.
    """
    logger = logging.getLogger()

    if err is not None:
        logger.error('{}'.format(err))
    else:
        message = 'Produced message. Topic: {}. Value: {}\n'.format(
            msg.topic(), 
            msg.value().decode('utf-8'))

        logger.info(message)


def push_messages(
    bootstrap_servers='',
    message_count=10, 
    topic='test', 
    sleep_time=3, 
    receipt_callback=cb_receipt):
    """Push a number of messages to a topic.
    """

    logger = logging.getLogger()

    logger.info('bootstrap_servers: ' + bootstrap_servers)
    logger.info('message_count: ' + str(message_count))
    logger.info('topic: ' + topic)
    logger.info('sleep_time: ' + str(sleep_time))

    # Get a Producer
    p = init_producer(bootstrap_servers=bootstrap_servers)
    if p is None:
        logger.error("Unable to obtain a Producer")
        return

    if message_count < 1:
        logger.error("message_count was less than 1")
        return

    # Generate and push fake messages
    for i in range(message_count):
        msg = generate_message()

        try:
            # Poll to process any receipts for past sent messages
            p.poll(1)

            # Asynchronously send the generated message to the Kafka topic
            p.produce(topic, msg.encode('utf-8'), callback=receipt_callback)

        except KafkaException as e:
            logger.exception(e)
            p.flush()
            return

        # Sleep for an interval
        time.sleep(sleep_time)

    # Flush any remaining messages
    p.flush()


