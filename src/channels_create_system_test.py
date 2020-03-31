'this file is the http testing for channels create'
import urllib
import json
from urllib.error import HTTPError # pylint: disable=C0412
import flask                        # pylint: disable=W0611

import pytest
from system_helper_functions import reg_user1, reset_workspace


#pylint compliant

#############################################################
#                   CHANNELS_CREATE                         #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_create():
    'successful case for channels create'
    reset_workspace()

    user1 = reg_user1()

    data = json.dumps({
        'token':user1['token'],
        'name': 'new_channel',
        'is_public': True
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req)

    assert payload['channel_id'] == 1

def test_long_name():
    'error case for channels create'
    reset_workspace()

    user1 = reg_user1()

    data = json.dumps({
        'token':user1['token'],
        'name': 'thisnameismorethantwntycharacters',
        'is_public': True
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/channels/create",
            data=data,
            headers={'Content-Type':'application/json'}
        ))
