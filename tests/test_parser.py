import os

import pytest

from parser import (
    _load_chat_from_android,
    _generate_report_data_from_android,
    generate_report_from_android,
    MessageAndroid
)

def test_should_load_chat_from_android():
    filename = "tests/assets/chat.txt"
    messages = _load_chat_from_android(filename)
    
    assert isinstance(messages, list)
    assert isinstance(messages[0], MessageAndroid)


@pytest.fixture
def message():
    raw_message = "23/03/2021 18:44 - ‎+55 21 98613-8297 entrou usando o link de convite deste grupo"
    return MessageAndroid(raw_message)


def test_should_parse_date(message):
    assert message.date == '23/03/2021'


def test_should_parse_hour(message):
    assert message.hour == '18:44'


def test_should_parse_number_raw(message):
    assert message.number_raw == '+55 21 98613-8297'


def test_should_parse_number(message):
    assert message.number == '5521986138297'


def test_should_parse_message(message):
    assert message.message == 'entrou usando o link de convite deste grupo'


def test_should_check_if_is_joined_message(message):
    assert message.is_joined is True
    assert message.is_left is False


@pytest.fixture
def message_left():
    raw_message = "23/03/2021 18:44 - ‎+55 21 98613-8297 saiu"
    return MessageAndroid(raw_message)


def test_should_check_if_is_left_message(message_left):
    assert message_left.is_left is True
    assert message_left.is_joined is False


def test_should_generate_report_data_from_android():
    directory = "tests/assets"
    report = _generate_report_data_from_android(directory)
    assert report == [
         {
            'date_joined': '23/03/2021',
            'date_left': '25/03/2021',
            'hour_joined': '18:44',
            'hour_left': '21:20',
            'number': '5521986138297'
        }
    ]

def test_should_generate_report_from_android():
    directory = "tests/assets"
    generate_report_from_android(directory)

    generated_file = os.path.join(directory, '00numbers.csv')
    assert os.path.exists(generated_file)
    os.remove(generated_file)
