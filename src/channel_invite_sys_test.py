'This is the system test for channel_invite'

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
from system_helper_functions import reg_user1, reg_user2, reg_user3, create_ch1, reset_workspace

BASE_URL = 'http://127.0.0.1:8080'

def test_channel_invite_successful():
    'Successful case'
    # channel_invite (POST)
    reset_workspace()

    # Register users
    user1 = reg_user1()
    token1 = user1['token']
    user2 = reg_user2()
    u_id2 = user2['u_id']
    # Create channel
    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    # Attempt to invite user2
    data = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id2
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/invite",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    payload = json.load(req)

    assert payload == {}

def test_channel_invite_invalid_channel():
    'Invalid channel case'
    reset_workspace()

    # Register users
    user1 = reg_user1()
    token1 = user1['token']
    user2 = reg_user2()
    u_id2 = user2['u_id']
    # Create channel
    create_ch1(user1)

    # Attempt to invite user2 to an invalid channel
    # Invalid channel_id = 100
    data = json.dumps({
        'token': token1,
        'channel_id': 100,
        'u_id': u_id2
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/invite",
            data=data,
            headers={'Content-Type': 'application/json'}
        ))

def test_channel_invite_invalid_userid():
    'Invalid user case'
    reset_workspace()

    # Register users
    user1 = reg_user1()
    token1 = user1['token']
    # Create channel
    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    # Attempt to invite a user with an invalid userID to a channel
    # Invalid u_id = 100
    data = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'u_id': 100
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/invite",
            data=data,
            headers={'Content-Type': 'application/json'}
        ))

def test_channel_invite_unauthorised():
    'User is not a member case'
    reset_workspace()

    # Register users
    user1 = reg_user1()
    user2 = reg_user2()
    token2 = user2['token']
    user3 = reg_user3()
    u_id3 = user3['u_id']

    # Create channel
    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    data = json.dumps({
        'token': token2,
        'channel_id': channel_id,
        'u_id': u_id3
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/invite",
            data=data,
            headers={'Content-Type': 'application/json'}
        ))

def test_channel_invite_existing_user():
    'Existing user case'
    reset_workspace()

    # Register users
    user1 = reg_user1()
    token1 = user1['token']
    user2 = reg_user2()
    u_id2 = user2['u_id']

    # Create channel
    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    # Invite
    data = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id2
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/invite",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    data2 = json.dumps({
        'token': token1,
        'channel_id': channel_id,
        'u_id': u_id2
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/invite",
            data=data2,
            headers={'Content-Type': 'application/json'}
        ))
