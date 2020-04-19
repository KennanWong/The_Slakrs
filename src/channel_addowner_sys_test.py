'This is the system test for channel_addowner'

# pylint: disable=W0611
# pylint: disable=C0412
# pylint: disable=W0611

# pylint compliant

import urllib
import json
from urllib.error import HTTPError
import flask
import pytest

import server
import channel
from system_helper_functions import reg_user1, reg_user2, reg_user3, create_ch1, reset_workspace

# channel_addowner (POST)

BASE_URL = 'http://127.0.0.1:4000'

def test_channel_addowner():
    'Normal case'
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
    data2 = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id2
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/addowner",
        data=data2,
        headers={'Content-Type': 'application/json'}
    ))
    payload = json.load(req)

    assert payload == {}

def test_already_owner():
    'Already owner case'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']
    user2 = reg_user2()
    u_id2 = user2['u_id']

    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    # Join
    data = json.dumps({
        'token': token1,
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

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/addowner",
            data=data2,
            headers={'Content-Type': 'application/json'}
        ))

def test_not_owner():
    'Non-owner case'
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    token2 = user2['token']
    user3 = reg_user3()
    token3 = user3['token']
    u_id3 = user3['u_id']

    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    # Join
    data = json.dumps({
        'token': token3,
        'channel_id': channel_id
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/join",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    data2 = json.dumps({
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id3
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/addowner",
            data=data2,
            headers={'Content-Type': 'application/json'}
        ))

def test_invalid_channel():
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
        'token': token1,
        'channel_id': 100,
        'u_id': u_id2
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/addowner",
            data=data3,
            headers={'Content-Type': 'application/json'}
        ))
