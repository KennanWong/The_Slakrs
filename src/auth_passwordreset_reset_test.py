'this file is the integration tests for auth passwordreset reset'

import pytest

import auth
from other import workspace_reset
from test_helper_functions import reg_user1, id_generator
from error import InputError
from data_stores import get_reset_code_store, get_auth_data_store



#############################################################
#                   AUTH_PASSWORDRESET_RESET                #
#############################################################
def test_reset():
    'testing functionability of passwordreset request'

    workspace_reset()

    user1 = reg_user1()
    reset_code = id_generator()

    # auth.request({
    #      'email': 'Kennan@gmail.com'
    # })

    auth.reset({
        'reset_code': reset_code,
        'new_password': 'thisiscool'
    })

    auth_store = get_auth_data_store()

    password_check = 0 #if new password is in auth store let = 1

    for i in auth_store:
        if i['password'] == 'thisiscool':
            password_check = 1

    assert password_check is 1

def test_invalid_password():
    'error case'

    workspace_reset()

    user1 = reg_user1()

    reset_code = id_generator()

    auth.request({
        'email': 'Kennan@gmail.com'
    })

    with pytest.raises(InputError):
        auth.reset({
            'reset_code': reset_code,
            'new_password': 'a'
        })

def test_invalid_resetcode():
    'error case'

    workspace_reset()

    user1 = reg_user1()

    auth.request({
        'email': 'Kennan@gmail.com'
    })

    with pytest.raises(InputError):
        auth.reset({
            'reset_code': 'ABCD',
            'new_password': 'thisiscool'
        })