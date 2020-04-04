'this file is the http testing for standup start'

import urllib
import json
from datetime import datetime, timedelta
import flask                                        # pylint: disable=W0611
from urllib.error import HTTPError                  # pylint: disable=C0412, C0411

import pytest
from system_helper_functions import reg_user1, reset_workspace, create_ch1

#pylint compliant

#############################################################
#                   STANDUP_START                           #
#############################################################

BASE_URL = 'http://127.0.0.1:5005'

def test_start():
    'successful case'
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
    payload = json.load(req)

    length = 30
    time_finish = (datetime.now() + timedelta(seconds=length)).strftime("%H:%M:%S")
    assert payload['time_finish'] == time_finish

def test_invalid_id():
    'error case'
    reset_workspace()

    user1 = reg_user1()


    data = json.dumps({
        'token': user1['token'],
        'channel_id': 100,
        'length': 30
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/standup/start",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_already_active():
    'error case'
    reset_workspace()


    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 30
    }).encode('utf-8')

    urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/standup/start",                    # pylint: disable=C0330
            data=data,                                      # pylint: disable=C0330
            headers={'Content-Type':'application/json'}     # pylint: disable=C0330
        ))

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/standup/start",
            data=data,
            headers={'Content-Type':'application/json'}
        ))                                                   # pylint: disable=C0304