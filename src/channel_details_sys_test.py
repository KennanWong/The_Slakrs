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

BASE_URL = 'http://127.0.0.1:4000'

def test_channel_details():
    'Getting details'
    reset_workspace()

    user1 = reg_user1()
    token1 = user1['token']
    u_id1 = user1['u_id']

    channel1 = create_ch1(user1)
    channel_id = channel1['channel_id']

    req = urllib.request.Request(
        f"{BASE_URL}/channel/details?token="+str(token1)+"&channel_id="+str(channel_id)
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

    req = urllib.request.Request(
        f"{BASE_URL}/channel/details?token="+str(token1)+"&channel_id=100"
    )
    req.get_method = lambda: 'GET'

    # Attempt to get details of an invalid channel
    # Invalid channel_id = 100
    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))

def test_channel_details_unauthorised():
    'User is not a member case'
    reset_workspace()

    # Register users
    user1 = reg_user1()
    user2 = reg_user2()
    token2 = user2['token']

    channel1 = create_ch1(user1)
    channel_id = channel1['channel_id']

    req = urllib.request.Request(
        f"{BASE_URL}/channel/details?token="+str(token2)+"&channel_id="+str(channel_id)
    )
    req.get_method = lambda: 'GET'

	# AccessError when we try to get details of channel where the user isn't a member
    # user2 isn't a member
    with pytest.raises(HTTPError):
        json.load(urllib.request.urlopen(req))
