from ensurepip import bootstrap
import pytest

from producer.config import settings
from producer.producer import init_producer, generate_message, push_messages

from confluent_kafka import KafkaException, Producer

def test_init_producer():
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
            'result_type': Producer
        }
    ]

    _stadard_tests(tests, init_producer)

def test_generate_message():
    tests = [
        # TEST empty params
        {
            'kwargs': {},
            'result_type': str
        }
    ]

    _stadard_tests(tests, generate_message)

def test_push_messages():
    tests = [
        # TEST empty params (no bootstrap server)
        {
            'kwargs': {},
            'exception': Exception
        },
        # TEST message count less than 1
        {
            'kwargs': {'message_count': 0, 'sleep_time': 0},
            'exception': Exception
        },
        # TEST blank topic
        {
            'kwargs': {'topic': None, 'sleep_time': 0},
            'exception': Exception
        },
        # TEST valid bootstrap servers
        {
            'kwargs': {'bootstrap_servers': settings.get('ARG_BOOTSTRAP')},
            'result': None
        }
    ]

    _stadard_tests(tests, push_messages)


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

