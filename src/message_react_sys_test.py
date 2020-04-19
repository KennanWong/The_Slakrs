'''
Pytest file to test message_react on a system level
'''

# pylint: disable=W0611

import urllib
import json
from urllib.error import HTTPError

import flask
import pytest

from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2, send_msg1, invite_to_channel


#############################################################
#                   MESSAGE_REACT                           #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_react1():
    '''
    Test a valid use of react on your own message
    '''
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'react_id': 1
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/react",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    payload = json.load(req)

    assert payload == {}


def test_react2():
    '''
    Test another user in a channel attempting to react to another person message
    '''
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    invite_to_channel(user1, user2, channel1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user2['token'],
        'message_id': msg1['message_id'],
        'react_id': 1
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/react",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    payload = json.load(req)

    assert payload == {}

def test_invalid_msg_id():
    '''
    Test reacting with an invalid message id
    '''
    reset_workspace()

    user1 = reg_user1()

    data = json.dumps({
        'token': user1['token'],
        'message_id': 1,
        'react_id': 1
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/react",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_invalid_react_id():
    '''
    Test a user reacting with an invalid reactId
    '''
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'react_id': 2
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/react",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_not_in_channel():
    '''
    Test a user reacting to a message in a channel they
    are not a part of
    '''
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user2['token'],
        'message_id': msg1['message_id'],
        'react_id': 1
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/react",
            data=data,
            headers={'Content-Type':'application/json'}
        ))
