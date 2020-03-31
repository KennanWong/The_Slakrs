'This is the system test for channel_messages'

import urllib
import json
from urllib.error import HTTPError
import flask
import pytest

import server
import channel
from system_helper_functions import reg_user1, reg_user2, reg_user3, create_ch1, reset_workspace

BASE_URL = 'http://127.0.0.1:8080'

def test_channel_messages():
# channel_messages (GET)
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data=[],
        headers={'Content-Type': 'application/json'}
    ))
    response = urllib.request.urlopen(f"{BASE_URL}/channel/messsages")
    payload = json.load(response)
    '''
    assert payload == {
        "messages": 
        "start": start,
        "end": end
    }
    '''