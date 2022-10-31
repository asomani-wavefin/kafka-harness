# test_consumer.py

import pytest

from consumer.config import settings
from consumer.consumer import init_consumer, receive_messages

from confluent_kafka import KafkaException, Consumer


def test_init_consumer():
    tests = [
        # TEST empty bootstrap server
        {
            'kwargs': {'bootstrap_servers': ''},
            'result': None
        },
        # TEST invalid bootstrap server
        {
            'kwargs': {'bootstrap_servers': 'nohost:1111'},
            'result': None
        },
        # TEST valid bootstrap server
        {
            'kwargs': {'bootstrap_servers': settings.get('ARG_BOOTSTRAP')},
            'result_type': Consumer
        }
    ]

    _stadard_tests(tests, init_consumer)

def test_receive_messages():
    tests = [
        # TEST empty params (no bootstrap server)
        {
            'kwargs': {},
            'exception': Exception
        },
        # TEST topic empty
        {
            'kwargs': {'bootstrap_servers': settings.get('ARG_BOOTSTRAP'), 'topic': ''},
            'exception': Exception
        },
        # TEST topic is None
        {
            'kwargs': {'bootstrap_servers': settings.get('ARG_BOOTSTRAP'), 'topic': None},
            'exception': Exception
        },
        # TEST valid bootstrap servers and topic
        {
            'kwargs': {'bootstrap_servers': settings.get('ARG_BOOTSTRAP'), 'topic': settings.get('ARG_TOPIC')},
            'result': None
        }
    ]

    _stadard_tests(tests, receive_messages)



#######

def _stadard_tests(tests, f):
    for test in tests:
        kwargs = test.get('kwargs')
        exception = test.get('exception', None)
        result = test.get('result', None)
        result_type = test.get('result_type', None)

        if exception is not None:
            with pytest.raises(exception):
                retval = f(**kwargs)
        else:                
            retval = f(**kwargs)

            if result_type is not None:
                assert isinstance(retval, result_type)
            if result is not None:
                assert retval == result

