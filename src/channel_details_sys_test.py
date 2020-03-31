'This is the system test for channel_details'

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
import channels
from system_helper_functions import reg_user1, reg_user2, create_ch1, reset_workspace

# pylint: disable=C0301

# pylint compliant

BASE_URL = 'http://127.0.0.1:8080'

def test_channel_details():
    'Getting details'
    # channel_details (GET)
    reset_workspace()

    user1 = reg_user1()
    u_id1 = user1['u_id']

    req = urllib.request.Request(
        f"{BASE_URL}/channel/details?token=6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b&channel_id=1"
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
    data = json.dumps({
        'token': token1,
        'channel_id': 100,
        'u_id': u_id2
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channel/details",
            data=data,
            headers={'Content-Type': 'application/json'}
        ))
