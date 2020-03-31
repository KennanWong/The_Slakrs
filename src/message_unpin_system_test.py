'this file is the http testing for message unpin'

import urllib
import json
from urllib.error import HTTPError      # pylint: disable=C0412
import flask                            # pylint: disable=W0611


import pytest
from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2, send_msg1

#pylint  ompliant
#############################################################
#                   MESSAGE_UNPIN                           #
#############################################################

BASE_URL = 'http://127.0.0.1:5005'

def test_unpin():
    '''
    Test a valid use of pin on your own message
    '''
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(  # pylint: disable=W0611, W0612
        f"{BASE_URL}/message/pin",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    data1 = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
    }).encode('utf-8')

    req1 = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/unpin",
        data=data1,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req1)
    assert payload == {}

def test_already_unpinned():
    'test error case'
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],

    }).encode('utf-8')

    urllib.request.urlopen(urllib.request.Request(
    f"{BASE_URL}/message/pin",                          # pylint: disable=C0330
    data=data,                                          # pylint: disable=C0330
    headers={'Content-Type':'application/json'}         # pylint: disable=C0330
    ))

    data1 = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
    }).encode('utf-8')

    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/unpin",
        data=data1,
        headers={'Content-Type':'application/json'}
    ))

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/unpin",
            data=data1,
            headers={'Content-Type':'application/json'}
        ))

def test_invalid_id():
    'test error case'
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],

    }).encode('utf-8')

    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/pin",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    data1 = json.dumps({
        'token': user1['token'],
        'message_id': 1,
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/unpin",
            data=data1,
            headers={'Content-Type':'application/json'}
        ))

def test_unauth_member():
    'test error case'
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    user2 = reg_user2()

    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
    }).encode('utf-8')

    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/pin",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    data1 = json.dumps({
        'token': user2['token'],
        'message_id': 1,
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/unpin",
            data=data1,
            headers={'Content-Type':'application/json'}
        ))

'''
def test_unauth_owner():
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()

    channel1 = create_ch1(user1)

    invite_to_channel(user1, user2, channel1)
    msg1 = send_msg1(user1, channel1)

    data = json.dumps({
        'token': user1['token'],
        'message_id': msg1['message_id'],
    }).encode('utf-8')

    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/pin",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    data1 = json.dumps({
        'token': user2['token'],
        'message_id': 1,
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/message/unpin",
            data=data1,
            headers={'Content-Type':'application/json'}
        ))
'''                                                             # pylint: disable=W0105, C0304