import urllib.request
import json
from test_helper_functions import reg_user1, reg_user2, register_and_create
import pytest

BASE_URL = 'http://127.0.0.1:4999'

ret = register_and_create()
user1 = ret['user']
channelInfo = ret['channel']
channel_id = channelInfo['channel_id']
user2 = reg_user2()

token = user1['token']
u_id = user1['u_id']
token2 = user2['token']

def test_channel_invite():
# channel_invite (POST)
    data = json.dumps({
        'token': token,
        'channel_id': channel_id,
        'u_id': u_id
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/channel/invite",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    response = urllib.request.urlopen(req)
    payload = json.load(response)

    assert payload == {}

def test_channel_details():
# channeL_details (GET)
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
    data = json.dumps({
        'token': token2, # second user leaving
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
    data = json.dumps({
        'token': token2, # second user joining
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
