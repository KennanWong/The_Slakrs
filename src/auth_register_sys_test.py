'''
Pytest file to test functionality of auth_register on a system
level
'''
import urllib
import json
import flask
from urllib.error import HTTPError
import pytest

from system_helper_functions import reset_workspace



#############################################################
#                   AUTH_REGISTER                           #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_register1():
    '''
    Test a valid case of auth/register
    '''
    reset_workspace()

    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/register",
        data=data,
        headers={'Content-Type':'application/json'}
    ))
    payload = json.load(req)

    # asserts that the u_id's of the one return matches the user found
    assert payload['u_id'] == 1



def test_invalid_email():
    '''
    Test registering a user with an invalid email
    '''
    reset_workspace()
    data = json.dumps({
        'email' : 'Kennan@.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_email_used():
    '''
    Test regiseting a user with an email that is already in use
    '''
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
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    # Attempt to register new user with the same email
    data2 = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Ken',
        'name_last': 'Wong'
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data2,
            headers={'Content-Type':'application/json'}
        ))

def test_short_pass():
    '''
    Test registering a user with a password that is too short
    '''
    reset_workspace()

    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong',
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }).encode('utf-8')
    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_short_first_name():
    '''
    Test regiseting a user with a first name that is too short
    '''
    reset_workspace()

    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'K',
        'name_last': 'Wong'
    }).encode('utf-8')
    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_short_last_name():
    '''
    Test registering a user with a last name that is too short
    '''
    reset_workspace()

    data = json.dumps({
        'email' : 'Kennan@gmail.com',
        'password': 'Wong123',
        'name_first': 'Kennan',
        'name_last': 'W'
    }).encode('utf-8')
    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={'Content-Type':'application/json'}
        ))


def test_register_double():
    '''
    Test when a user attempts to re-register themselves
    '''
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
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/register",
            data=data,
            headers={'Content-Type':'application/json'}
        ))
