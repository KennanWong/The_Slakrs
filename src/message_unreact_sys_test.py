'''
Pytest file to test message_unreact on a system level
'''
import urllib
import json
import flask
from urllib.error import HTTPError
import pytest

from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2, send_msg1, react_to_msg

#############################################################
#                   MESSAGE_UNREACT                         #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_unreact1():
    '''
    Test a valid case of message_unreact to a message they had sent
    '''
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)
    react_to_msg(user1, msg1, 1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'react_id': 1
    }).encode('utf-8')
    
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/unreact",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    payload = json.load(req)

    assert payload == {}
    
'''
def test_react2():
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    invite_to_channel(user1, user2, channel1)
    msg1 = send_msg1(user1, channel1)
    react_to_msg(user2, msg1, 1)

    data = json.dumps({
        'token': user2['token'],
        'message_id': msg1['message_id'],
        'react_id': 1
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/unreact", 
        data = data, 
        headers = {'Content-Type':'application/json'}
    ))

    payload = json.load(req)

    assert payload == {}
'''

def test_not_reacted():
    '''
    Test unreacting to a message they have already reacted to
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

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/unreact",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_invalid_msg_id():
    '''
    Test unreacting with an invalid message id
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
            f"{BASE_URL}/message/unreact",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_invalid_react_id():
    '''
    Test a user unreacting with an invalid reactId
    '''
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)
    react_to_msg(user1, msg1, 1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'react_id': 2
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/unreact",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_not_in_channel():
    '''
    Test a user unreacting to a message in a channel they
    are not a part of
    '''
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)
    react_to_msg(user1, msg1, 1)

    data = json.dumps({
        'token': user2['token'],
        'message_id': msg1['message_id'],
        'react_id': 1
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/unreact",
            data=data,
            headers={'Content-Type':'application/json'}
        ))
