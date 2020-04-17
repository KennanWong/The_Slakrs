'''
Pytest file to test auth_passwordreset on a system level
'''

import urllib
import json
from urllib.error import HTTPError
import flask
import pytest

from system_helper_functions import reg_user1, reset_workspace, id_generator


#############################################################
#                     AUTH_PASSWORDRESET_REQUEST            #
#############################################################

BASE_URL = 'http://127.0.0.1:8080'

def test_reset():
    '''
    Test valid case of test_password_request
    '''
    reset_workspace()

    user1 = reg_user1()

    reset_code = id_generator()

    data = json.dumps({
        'email': 'Kennan@gmail.com'
    }).encode('utf-8')

    req = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/passwordreset/request",
        data=data,
        headers={'Content-Type':'application/json'}
    ))

    data1 = json.dumps({
        'reset_code': reset_code,
        'new_password': 'thisiscool'
    }).encode('utf-8')

    req1 = urllib.request.urlopen(urllib.request.Request(
        f"{BASE_URL}/auth/passwordreset/reset",
        data=data1,
        headers={'Content-Type':'application/json'}
    ))

    payload = json.load(req1)
    assert payload == {}

def test_invalid_password():
    '''
    error case
    '''
    reset_workspace()

    user1 = reg_user1()

    reset_code = id_generator()

    data = json.dumps({
        'reset_code': reset_code,
        'new_password': 'a'
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/passwordreset/reset",
            data=data,
            headers={'Content-Type':'application/json'}
        ))

def test_invalid_resetcode():
    '''
    error case
    '''

    reset_workspace()

    user1 = reg_user1()

    data = json.dumps({
        'reset_code': 'ABCDEF',
        'new_password': 'thisiscool'
    }).encode('utf-8')

    with pytest.raises(HTTPError):
        urllib.request.urlopen(urllib.request.Request(
            f"{BASE_URL}/auth/passwordreset/reset",
            data=data,
            headers={'Content-Type':'application/json'}
        ))