import pytest
import urllib
import json
import flask
from urllib.error import HTTPError

import server
import auth
from system_helper_functions import reg_user1, reset_workspace, logout_user1
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
    response = reg_user1()
    
    # Logout that user
    logout_user1(response['token'])

    # Attempt to login that user
    data = json.dumps({
        'email': 'Kennan@gmail.com',
        'password': 'Wong123'
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/login", 
        data = data, 
        headers = {'Content-Type':'application/json'}
    ))
    payload = json.load(req)

    assert response['u_id'] == payload['u_id']
    assert response['token'] == payload['token']



def test_invalid_email():
    reset_workspace()
    
    # Register a user
    response = reg_user1()
    
    # Logout that user
    logout_user1(response['token'])

    data = json.dumps({
        'email': 'Kennan@.com',
        'password': 'Wong123'
    }).encode('utf-8')
    
    with pytest.raises(HTTPError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/login", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))

def test_wrong_email():
    reset_workspace()
    
    # Register a user
    response = reg_user1()
    
    # Logout that user
    logout_user1(response['token'])

    data = json.dumps({
        'email': 'Kennand@gmail.com',
        'password': 'Wong123'
    }).encode('utf-8')
    
    with pytest.raises(HTTPError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/login", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))

def test_wrong_pass():
    reset_workspace()
    
    # Register a user
    response = reg_user1()
    
    # Logout that user
    logout_user1(response['token'])

    data = json.dumps({
        'email': 'Kennan@gmail.com',
        'password': 'Wong321'
    }).encode('utf-8')
    
    with pytest.raises(HTTPError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/login", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))


