'''
Pytest file to test auth_login and its edge cases
'''
import pytest

import auth
from test_helper_functions import reg_user1
from data_stores import reset_auth_store
from error import InputError


#############################################################
#                   AUTH_LOGIN                              #
#############################################################


def test_login1():
    '''
    Test basic functionality of login
    '''
    reset_auth_store()
    user1 = reg_user1()

    auth.logout({
        'token': user1['token']
    })

    assert auth.login({'email':'Kennan@gmail.com', 'password':'Wong123'})['token'] == user1['token']


def test_invalid_email_login():
    '''
    Test login if provided an invalid login
    '''
    reset_auth_store()
    user1 = reg_user1()

    auth.logout({
        'token': user1['token']
    })
    with pytest.raises(InputError):
        auth.login({
            'email':'Kennan@com',
            'password':'Wong123'
        })

def test_wrong_email():
    '''
    Test login if provided with an incorrect email
    '''
    reset_auth_store()
    user1 = reg_user1()

    auth.logout({
        'token': user1['token']
    })
    with pytest.raises(InputError):
        auth.login({
            'email':'Nat@gmail.com',
            'password':'Wong123'
        })


def test_wrong_pass():
    '''
    Test login if provided with an incorrect pass
    '''
    reset_auth_store()
    user1 = reg_user1()

    auth.logout({
        'token': user1['token']
    })
    with pytest.raises(InputError):
        auth.login({
            'email':'Kenann@gmail.com',
            'password':'Wong123'
        })
