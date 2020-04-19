'This is the system test for channel_removeowner'

# pylint: disable=W0611
# pylint: disable=C0412

# pylint compliant

import urllib
import json
from urllib.error import HTTPError
import flask
import pytest

import server
import channel
from system_helper_functions import reg_user1, reg_user2, create_ch1, reset_workspace

# channel_removeowner (POST)

BASE_URL = 'http://127.0.0.1:8080'

def test_channel_removeowner():
    'Normal case'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']
    u_id1 = user1['u_id']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    # Join
    data = json.dumps({
        'token': token2,
        'channel_id': channel_id
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/join",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    # Addowner
    data2 = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id2
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/addowner",
        data=data2,
        headers={'Content-Type': 'application/json'}
    ))
    data3 = json.dumps({
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id1
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/removeowner",
        data=data3,
        headers={'Content-Type': 'application/json'}
    ))
    payload = json.load(req)

    assert payload == {}

def test_invalid_channel2():
    'Invalid channel case'
    reset_workspace()
    user1 = reg_user1()
    token1 = user1['token']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    # Join
    data = json.dumps({
        'token': token2,
        'channel_id': channel_id
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/join",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    # Addowner
    data2 = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id2
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/addowner",
        data=data2,
        headers={'Content-Type': 'application/json'}
    ))
    # Invalid channel_id = 100
    data3 = json.dumps({
        'token': token2,
        'channel_id': 100,
        'u_id': u_id2
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/removeowner",
            data=data3,
            headers={'Content-Type': 'application/json'}
        ))

def test_userid_not_owner():
    'User is not an owner case'
    reset_workspace()
    user1 = reg_user1()
    token1 = user1['token']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    # Join
    data = json.dumps({
        'token': token2,
        'channel_id': channel_id
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/join",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    # Addowner
    data2 = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id2
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/addowner",
        data=data2,
        headers={'Content-Type': 'application/json'}
    ))
    # Invalid user_id = 100
    data3 = json.dumps({
        'token': token2,
        'channel_id': channel_id,
        'u_id': 100
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/removeowner",
            data=data3,
            headers={'Content-Type': 'application/json'}
        ))

def test_not_owner2():
    'Non-owner case'
    reset_workspace()
    user1 = reg_user1()
    u_id1 = user1['u_id']
    user2 = reg_user2()
    token2 = user2['token']

    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    data = json.dumps({
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id1
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/removeowner",
            data=data,
            headers={'Content-Type': 'application/json'}
        ))
