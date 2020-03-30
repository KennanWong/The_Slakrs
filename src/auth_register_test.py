'''
Pytest file to test functionality of auth_register
'''

import pytest
import urllib
import json
import flask

import server
import auth
from other import workspace_reset
from data_stores import get_auth_data_store, reset_auth_store
from helper_functions import get_user_token
from error import InputError


#############################################################
#                   AUTH_REGISTER                           #
#############################################################

def test_register1():
    '''
    Test valid use of test_register
    '''
    workspace_reset()
    payload = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }

    result1 = auth.register(payload)

    auth_store = get_auth_data_store()

    assert result1 in auth_store
    return

def test_invalid_email_reg():
    '''
    Test auth.register on an invalid email
    '''
    workspace_reset()
    payload = {
        'email' : 'Kennan@com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }
    with pytest.raises(InputError):
        auth.register(payload)


def test_email_used():
    workspace_reset()
    payload = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }
    auth.register(payload)

    payload2 = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Ken',
        'name_last': 'Wong'
    }
    with pytest.raises(InputError):
        auth.register(payload2)


def test_short_pass():
    '''
    Test auth.register on a short pass
    '''
    workspace_reset()
    payload = {
        'email' : 'Kennan@gmail.com',
        'password': 'short',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }
    with pytest.raises(InputError):
        auth.register(payload)


def test_short_name():
    '''
    Test auth.register on a short first name
    '''
    workspace_reset()
    payload = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'K',
        'name_last': 'Wong'
    }
    with pytest.raises(InputError):
        auth.register(payload)


def test_short_last():
    '''
    Test auth.register on a short last name
    '''
    workspace_reset()
    payload = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'W'
    }
    with pytest.raises(InputError):
        auth.register(payload)


def test_register_double1():
    '''
    Test if a user tries to re register
    '''
    workspace_reset()
    payload = {
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }
    auth.register(payload)
   
    with pytest.raises(InputError):
        auth.register(payload)



#############################################################
#                   SYSTEM TESTS                            #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_sys_register2():
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data = [],  
        headers = {'Content-Type':'application/json'}
    ))
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

    # find a user with the returned token
    user = get_user_token(payload['token'])

    # asserts that the u_id's of the one return matches the user found
    assert payload['u_id'] == user['u_id']

'''
def test_sys_invalid_email():
    reset = req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/workspace/reset",
        data = [],  
        headers = {'Content-Type':'application/json'}
    ))
    data = json.dumps({
        'email' : 'Kennan@.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    with pytest.raises(InputError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))
'''