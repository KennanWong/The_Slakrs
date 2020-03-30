import urllib.request
import json
import pytest
import flask

import server
import auth
from system_helper_functions import reg_user1, reg_user2, create_ch1, reset_workspace
from other import workspace_reset
#from data_stores import get_auth_data_store, reset_auth_store
#from helper_functions import get_user_token
from error import InputError

BASE_URL = 'http://127.0.0.1:4999'

def test_channel_invite():
# channel_invite (POST)
    reset_workspace()
    
    # Register users
    response1 = reg_user1()
    response2 = reg_user2()
    token1 = response1['token']
    u_id2 = response2['u_id']
    channelInfo = create_ch1()
    channel_id = channelInfo['channel_id']

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

def test_channel_details():
# channeL_details (GET)
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data=[],
        headers={'Content-Type': 'application/json'}
    ))
    response = urllib.request.urlopen(f"{BASE_URL}/channel/details")
    payload = json.load(response)
    assert payload == {
        "name": 'The Slakrs',
        "owner_members": [{"u_id": 1, "name_first": "Hayden", "name_last": "Smith"}],
        "all_members": [{"u_id": 1, "name_first": "Hayden", "name_last": "Smith"}]
    }
'''
def test_channel_messages():
# channel_messages (GET)
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data=[],
        headers={'Content-Type': 'application/json'}
    ))
    response = urllib.request.urlopen(f"{BASE_URL}/channel/messsages")
    payload = json.load(response)
    assert payload == {
        "messages": 
        "start": start,
        "end": end
    }
'''
def test_channel_leave():
# channel_leave (POST)
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data=[],
        headers={'Content-Type': 'application/json'}
    ))
    data = json.dumps({
        'token': token2, # user2 leaving
        'channel_id': channel_id,
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/channel/leave",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    assert payload == {}

def test_channel_join():
# channnel_join (POST)
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data=[],
        headers={'Content-Type': 'application/json'}
    ))
    data = json.dumps({
        'token': token,
        'channel_id': channel_id,
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/channel/join",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    response = urllib.request.urlopen(req)
    payload = json.load(response)
    
    assert payload[''] == '{"name": "", "owner_members": "", "all_members": = ""}'

def test_channel_addowner():
# channel_addowner (POST)
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data=[],
        headers={'Content-Type': 'application/json'}
    ))
    data = json.dumps({
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/channel/addowner",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    assert payload[''] == {}

def test_channel_removeowner():
# channel_removeowner (POST)
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data=[],
        headers={'Content-Type': 'application/json'}
    ))
    data = json.dumps({
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    }).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/channel/removeowner",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    assert payload[''] == {}
