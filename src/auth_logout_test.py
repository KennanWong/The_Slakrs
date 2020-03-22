from auth import *
import user
import pytest
import other
from error import InputError
'''
#############################################################
#                   AUTH_LOGOUT                             #      
#############################################################
'''
# assume register and login works
# assume that users_all functions, and is able to generate u_id

def test_logout1():
    result1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    result2 = auth_login('John.smith@gmail.com', 'password1')
    user1_tk = result2['token']
    assert auth_logout(user1_tk)['is_success'] == True
    

def test_bad_token():
    result1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    result2 = auth_login('John.smith@gmail.com', 'password1')
    user1_tk = result2['token']

    bad_tk = str(int(user1_tk) + 1)
    
    assert auth_logout(bad_tk)['is_success'] == False