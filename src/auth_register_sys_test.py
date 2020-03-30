'''
Pytest file to test functionality of auth_register on a system 
level
'''

import pytest
import urllib
import json
import flask
from urllib.error import HTTPError

import server
import auth
from system_helper_functions import reset_workspace
from other import workspace_reset
from data_stores import get_auth_data_store, reset_auth_store
from helper_functions import get_user_token
from error import InputError


#############################################################
#                   AUTH_REGISTER                           #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_register1():
    reset_workspace()

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

    # asserts that the u_id's of the one return matches the user found
    assert payload['u_id'] == 1



def test_invalid_email():
    reset_workspace()
    data = json.dumps({
        'email' : 'Kennan@.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    with pytest.raises(HTTPError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))

def test_email_used():
    reset_workspace()

    # Register user first
    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register", 
        data = data, 
        headers = {'Content-Type':'application/json'}
    ))

    # Attempt to register new user with the same email
    data2 = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Ken',
        'name_last': 'Wong'
    }).encode('utf-8')
    with pytest.raises(HTTPError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))

def test_short_pass():
    reset_workspace()

    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    with pytest.raises(HTTPError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))

def test_short_first_name():
    reset_workspace()

    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'K',
        'name_last': 'Wong'
    }).encode('utf-8')
    with pytest.raises(HTTPError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))

def test_short_last_name():
    reset_workspace()

    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'W'
    }).encode('utf-8')
    with pytest.raises(HTTPError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))


def test_register_double():
    reset_workspace()

    # Register user first
    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register", 
        data = data, 
        headers = {'Content-Type':'application/json'}
    ))

    with pytest.raises(HTTPError):
        req = urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register", 
            data = data, 
            headers = {'Content-Type':'application/json'}
        ))

