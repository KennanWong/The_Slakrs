'This is the system test for channel_details'

# pylint: disable=W0611
# pylint: disable=C0412
# pylint: disable=C0301

# pylint compliant

import urllib
import json
from urllib.error import HTTPError
import flask
import pytest

import server
import channel
import channels
from system_helper_functions import reg_user1, reg_user2, create_ch1, reset_workspace

# channel_details (GET)

BASE_URL = 'http://127.0.0.1:8080'

def test_channel_details():
    'Getting details'
    reset_workspace()

    user1 = reg_user1()
    u_id1 = user1['u_id']

    channel1 = create_ch1(user1)

    req = urllib.request.Request(
        f"{BASE_URL}/channel/details?token="+str(user1['token'])+"&channel_id="+str(channel1['channel_id'])
    )
    req.get_method = lambda: 'GET'

    payload = json.load(urllib.request.urlopen(req))

    assert payload['name'] == 'new_channel'
    assert payload['owner_members'] == [{
        "u_id": u_id1,
        "name_first": 'Kennan',
        "name_last": 'Wong'
    }]
    assert payload['all_members'] == [{
        "u_id": u_id1,
        "name_first": 'Kennan',
        "name_last": 'Wong'
    }]

def test_channel_details_invalid_channel():
    'Invalid channel case'
    reset_workspace()

    # Register users
    user1 = reg_user1()
    token1 = user1['token']
    user2 = reg_user2()
    u_id2 = user2['u_id']

    # Attempt to get details of an invalid channel
    # Invalid channel_id = 100

    with pytest.raises(HTTPError):
        req = urllib.request.Request(
            f"{BASE_URL}/channel/details?token="+str(user1['token'])+"&channel_id=1"
        )
        req.get_method = lambda: 'GET'
        json.load(urllib.request.urlopen(req))
