'This is the system test for channel_messages'

import urllib
import json
from urllib.error import HTTPError
import flask
import pytest

import server
import channel
from system_helper_functions import reg_user1, reg_user2, reg_user3, create_ch1, reset_workspace

# channel_messages (GET)

BASE_URL = 'http://127.0.0.1:808'

def test_channel_messages():
    'Getting messages'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']

    channel1 = create_ch1(user1)
    channel_id = channel1['channel_id']

    req = urllib.request.Request(
        f"{BASE_URL}/channel/messages?token="+str(token1)+"&channel_id="+str(channel_id)+"&start="+int(start)
    )
    req.get_method = lambda: 'GET'

    payload = json.load(urllib.request.urlopen(req))

    assert payload['messages'] == []
    assert payload['start'] == 0
    assert payload['end'] == -1

def test_channel_messages_invalid_channel():
    'Invalid channel case'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']
    user2 = reg_user2()
    token2 = user2['token']

    channel1 = create_ch1(user1)
    channel_id = channel1['channel_id']

    # Send a message
    data = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'message': "hello"
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    req = urllib.request.Request(
        f"{BASE_URL}/channel/messages?token="+str(token2)+"&channel_id=100"+"&start="+int(start)
    )
    req.get_method = lambda: 'GET'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))

def test_channel_messages_start_excess():
    'Start >= total messages case'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']

    channel1 = create_ch1(user1)
    channel_id = channel1['channel_id']

    # Send a message
    data = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'message': "hello"
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    req = urllib.request.Request(
        f"{BASE_URL}/channel/messages?token="+str(token1)+"&channel_id="+str(channel_id)+"&start=50"
    )
    req.get_method = lambda: 'GET'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))

def test_channel_messages_unauthorised():
    'User is not a member case'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']

    channel1 = create_ch1(user1)
    channel_id = channel1['channel_id']

    # Send a message
    data = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'message': "hello"
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/message/send",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    req = urllib.request.Request(
        f"{BASE_URL}/channel/messages?token="+str(token1)+"&channel_id="+str(channel_id)+"&start=50"
    )
    req.get_method = lambda: 'GET'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))

def test_others1():
    'Other errors, when start is not of type int'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']

    channel1 = create_ch1(user1)
    channel_id = channel1['channel_id']
#CANT BE TYPE INT
    req = urllib.request.Request(
        f"{BASE_URL}/channel/messages?token="+str(token1)+"&channel_id="+str(channel_id)+"&start=asdf"
    )
    req.get_method = lambda: 'GET'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))

def test_others2():
    'Other errors, when start is negative'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']

    channel1 = create_ch1(user1)
    channel_id = channel1['channel_id']

    req = urllib.request.Request(
        f"{BASE_URL}/channel/messages?token="+str(token1)+"&channel_id="+str(channel_id)+"&start=-1"
    )
    req.get_method = lambda: 'GET'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))
