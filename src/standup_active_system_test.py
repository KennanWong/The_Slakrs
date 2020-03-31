import urllib
import json
import flask
from urllib.error import HTTPError

import pytest
from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2, send_msg1

import time
from datetime import datetime, timedelta
from helper_functions import addSecs


#############################################################
#                   STANDUP_ACTIVE                          #
#############################################################

BASE_URL = 'http://127.0.0.1:5005'

def test_active():
     
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data1 = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 30
    }).encode('utf-8')

    req1 = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/standup/start",
        data=data1,
        headers={'Content-Type':'application/json'}
    ))
    
    data = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
    }).encode('utf-8')

    req = urllib.request.Request(
        f"{BASE_URL}/standup/active",
        data=data,
        headers={'Content-Type':'application/json'}
    )

    req.get_method = lambda: 'GET'
    response = json.load(urllib.request.urlopen(req))

    assert response['is_active'] is True


    #length = 30
    #time_finish = (datetime.now() + timedelta(seconds=length)).strftime("%H:%M:%S")
   # assert response['time_finish'] == time_finish
    

def test_invalid_id():
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 30
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/standup/start",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    data1 = json.dumps({
        'token': user1['token'],
        'channel_id': 100,
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/standup/active",
            data=data1,
            headers={'Content-Type':'application/json'}
        ))

