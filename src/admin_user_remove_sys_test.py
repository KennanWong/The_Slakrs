'This is the system test for admin_user_remove'

import urllib
import json
from urllib.error import HTTPError
import flask
import pytest

import server
import channel
from system_helper_functions import reg_user1, reg_user2, reg_user3, create_ch1, reset_workspace

BASE_URL = 'http://127.0.0.1:8080'

def test_admin_user_remove_successful():
    'Successful case'
    # admin_user_remove (DELETE)
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

    data2 = json.dumps({
        'token': token1,
        'u_id': u_id2
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/admin/user/remove",
        data=data2,
        headers={'Content-Type': 'application/json'}
    )
    req.get_method = lambda: 'DELETE'
    payload = json.load(urllib.request.urlopen(req))

    assert payload == {}

def test_invalid_userid():
    'Invalid user case'
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

    data3 = json.dumps({
        'token': token2,
        'u_id': 100
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/admin/user/remove",
        data=data3,
        headers={'Content-Type': 'application/json'}
    )
    req.get_method = lambda: 'DELETE'

    with pytest.raises(HTTPError):
        '''
        req = urllib.request.Request(
        f"{BASE_URL}/admin/user/remove",
        data=data3,
        headers={'Content-Type': 'application/json'}
        )
        req.get_method = lambda: 'DELETE'
        '''
        json.load(urllib.request.urlopen(req))

def test_unauthorised_slackr():
    'Authorised user is not an owner of slackr case'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']
    u_id1 = user1['u_id']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel_info = create_ch1(user1)
    channel_id = channel_info['channel_id']

    data2 = json.dumps({
        'token': token2,
        'u_id': u_id1
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/admin/user/remove",
        data=data2,
        headers={'Content-Type': 'application/json'}
    )
    req.get_method = lambda: 'DELETE'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))
