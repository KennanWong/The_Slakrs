'this file is the http testing for standup active'

import urllib
import json
from urllib.error import HTTPError  # pylint: disable=C0412
import flask                     # pylint: disable=W0611


import pytest
from system_helper_functions import reg_user1, reset_workspace, create_ch1

#pylint compliant
#############################################################
#                   STANDUP_ACTIVE                          #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_active():
    'successful case'
    reset_workspace()

    user1 = reg_user1()
    channel1 = create_ch1(user1)

    data1 = json.dumps({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'length': 30
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
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


def test_invalid_id():
    'error test'
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

    req = urllib.request.Request(
            f"{BASE_URL}/standup/active",                   # pylint: disable=C0330
            data=data1,                                     # pylint: disable=C0330
            headers={'Content-Type':'application/json'}     # pylint: disable=C0330
    )

    req.get_method = lambda: 'GET'

    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))
