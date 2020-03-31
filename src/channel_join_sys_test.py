'This is the system test for channel_join'

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
from system_helper_functions import reg_user1, reg_user2, create_ch1, create_pvt_ch, reset_workspace

BASE_URL = 'http://127.0.0.1:8080'

def test_channel_join():
    'Normal join case'
    # channnel_join (POST)
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']

    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    data = json.dumps({
        'token': token1,
        'channel_id': channel_id
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channel/join",
        data=data,
        headers={'Content-Type': 'application/json'}
    ))
    payload = json.load(req)

    assert payload == {}

def test_channel_join_invalid_channel():
    'Invalid channel case'
    reset_workspace()

    user2 = reg_user2()
    token2 = user2['token']

    # User attempting to join an invalid channel
    # Invalid channel_id = 100
    data = json.dumps({
        'token': token2,
        'channel_id': 100
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/join",
            data=data,
            headers={'Content-Type': 'application/json'}
        ))

def test_channel_join_private():
    'Privat channel case'
    reset_workspace()

    user1 = reg_user1()
    user2 = reg_user2()
    token2 = user2['token']
    pvt_channel = create_pvt_ch(user1)
    channel_id = pvt_channel['channel_id']

    data = json.dumps({
        'token': token2,
        'channel_id': channel_id
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/join",
            data=data,
            headers={'Content-Type': 'application/json'}
        ))
