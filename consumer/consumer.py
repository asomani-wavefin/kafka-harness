# consumer.py
"""Primary module for the consumer package

Parses command line arguments and calls main functionality.

Available functions:
- main: Main execution path. Parses the command line and delegates accordingly.

"""

__version__ = "0.2.0"

from confluent_kafka import KafkaException, Consumer
import argparse
import logging

from .config import settings


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

    # Consumer variables
    parser.add_argument('--bootstrap', action="store", type=ascii, default=settings.get('ARG_BOOTSTRAP'), help="comma-separated list for bootstrap.servers")
    parser.add_argument('--topic', action="store", type=ascii, default=settings.get('ARG_TOPIC'), help="topic from which messages will be received")

    # Parse the command line and call the command
    try:
        args = parser.parse_args()

        # verbose option increases the logger visibility
        if args.verbose:
            logger.setLevel(settings.get('VERBOSE_LOG_LEVEL'))
            print("output mode set to VERBOSE\n")
        
        receive_messages(
            args.bootstrap.strip("\'"), 
            args.topic.strip("\'"))

    except:
        print("An error occured")
        exit(1)

    finally:
        print("")

    exit(0)


def receive_messages(
    bootstrap_servers='',
    topic='test'):

    logger = logging.getLogger()

    logger.info('bootstrap_servers: ' + bootstrap_servers)
    logger.info('topic: ' + topic)

    # Get a Consumer
    if bootstrap_servers is None or len(bootstrap_servers) < 1:
        err_msg = "bootstrap servers cannot be blank"
        logger.error(err_msg)
        raise Exception(err_msg)
        return
        
    c = init_consumer(bootstrap_servers=bootstrap_servers)
    if c is None:
        err_msg = "unable to obtain a Consumer"
        logger.error(err_msg)
        raise Exception(err_msg)
        return

    try:
        # Subscribe to topic
        if topic is None or len(topic) < 1:
            err_msg = "topic cannot be blank"
            logger.error(err_msg)
            raise Exception(err_msg)
            return
        c.subscribe([topic])

        while True:
            msg = c.poll(1.0) #timeout
            if msg is None:
                logger.debug('no message')
                continue
            if msg.error():
                logger.error('{}'.format(msg.error()))
                continue

            msg_content = msg.value().decode('utf-8')
            print(msg_content)

    except KafkaException as e:
        logger.exception(e)
        return

    finally:
        c.close()


def init_consumer(bootstrap_servers='') -> Consumer:
    logger = logging.getLogger()
    logger.info('Initiating Kafka Consumer...')

    try:
        c = Consumer(
            {
                'bootstrap.servers': bootstrap_servers,
                'group.id': settings.get('KAFKA_group.id'),
                'auto.offset.reset': settings.get('KAFKA_auto.offset.reset')
            })
        if c is None:
            logger.critical('Failed to initiate Kafka Consumer!')
            return None

    except KafkaException as e:
        logger.exception(e)
        return None

    logger.info('Kafka Consumer successfully initiated.')
    return c


