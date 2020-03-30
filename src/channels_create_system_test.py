import urllib
import json
import flask
from urllib.error import HTTPError

import pytest
from system_helper_functions import reg_user1, reset_workspace, create_ch1
from system_helper_functions import reg_user2, send_msg1


BASE_URL = 'http://127.0.0.5002'

#############################################################
#                   CHANNELS_CREATE                         #
#############################################################


def test_create(user):
    reset_workspace()

    data = json.dumps({
        'token': user['token'],
        'name': 'Slackrs',
        'is_public': True
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/channels/create", 
        data = data, 
        headers = {'Content-Type':'application/json'}
    ))
    payload = json.load(req)

    assert payload['channel_id'] == 1

#def test_long_name():



