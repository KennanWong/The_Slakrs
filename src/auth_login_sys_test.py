'''
Pytest file to test auth_login on a system level
'''

import urllib
import json
import flask
from urllib.error import HTTPError
import pytest

from system_helper_functions import reg_user1, reset_workspace, logout_user1


#############################################################
#                     AUTH_LOGIN                            #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_login():
    '''
    Test valid case of test_login
    '''
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
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req)

    assert response['u_id'] == payload['u_id']
    assert response['token'] == payload['token']



def test_invalid_email():
    '''
    Test auth/login on an invalid email
    '''

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
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/login",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_wrong_email():
    '''
    Test auth/login with an incorrect email
    '''

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
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/login",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_wrong_pass():
    '''
    Test auth/login with an incorrect password
    '''

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
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/login",
            data=data,
            headers={'Content-Type':'application/json'}
        ))
