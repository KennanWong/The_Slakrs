import pytest
import urllib
import json
import flask

import server
import auth
from system_helper_functions import reg_user1, reset_workspace
from other import workspace_reset
from data_stores import get_auth_data_store, reset_auth_store
from helper_functions import get_user_token
from error import InputError


#############################################################
#                   AUTH_LOGOUT                             #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_logout1():
    reset_workspace()
    payload = reg_user1()

    data2 = json.dumps({
        'token': payload['token']
    }).encode('utf-8')

    req2 = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/logout", 
        data = data2, 
        headers = {'Content-Type':'application/json'}
    ))

    payload2 = json.load(req2)

    # asserts that the u_id's of the one return matches the user found
    assert payload2['is_success'] is True


