'''
Pytest file to test functionality of auth_logout
'''

import auth
from test_helper_functions import reg_user1, reg_user2
from data_stores import reset_auth_store

#############################################################
#                   AUTH_LOGOUT                             #
#############################################################


def test_logout1():
    '''
    Test a valid use case of auth.logout
    '''
    reset_auth_store()
    user1 = reg_user1()
    assert auth.logout(user1) == True


def test_bad_token():
    '''
    Test logout on a bad token
    '''
    reset_auth_store()
    reg_user1()

    user2 = reg_user2()
    auth.logout(user2)

    assert auth.logout(user2) == False

