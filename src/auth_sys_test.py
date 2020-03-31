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
#                     AUTH_LOGIN                            #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_login():
    reset_workspace()

    # Register a user
    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register", 
        data = data, 
        headers = {'Content-Type':'application/json'}
    ))
    payload = json.load(req) 
    token = payload['token']
    
    # Logout that user
    data2 = json.dumps({
        'token': payload['token']
    }).encode('utf-8')

    req2 = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/logout", 
        data = data2, 
        headers = {'Content-Type':'application/json'}
    ))

    # Attempt to login that user
    data3 = json.dumps({
        'email': 'Kennan@gmail.com',
        'password': 'Wong123'
    }).encode('utf-8')
    req3 = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/login", 
        data = data3, 
        headers = {'Content-Type':'application/json'}
    ))
    payload3 = json.load(req3)

    assert payload['u_id'] == payload3['u_id']
    assert payload['token'] == payload3['token']

