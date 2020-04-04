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
