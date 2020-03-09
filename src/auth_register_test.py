from auth import *
import user
import pytest
import other
from error import InputError

'''
#############################################################
#                   AUTH_REGISTER                           #      
#############################################################
'''

#assumes users_all functions
#assumes that registers, checkes users_all for an existing email address
#assumes that a check is in place to see if an email is valid or not
#assumes that length of the password is checked during register function
#assumes that the length of a first name is checked during register function
#assumes that the length of a last name is checked during register function

def test_register1():
    result1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    result2 = other.users_all(result1['token'])
    
    registered = 0

    for a in result2['users']:
        
        if (int(result1['u_id']) == int(a['u_id'])):
            registered = 1
    
    assert registered == 1

    

def test_invalid_email_reg():
    with pytest.raises(InputError):
        result1 = auth_register('John.smith@com', 'password1', 'John', 'Smith')

def test_email_used():
    result1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    with pytest.raises(InputError):
        result2 = auth_register('John.smith@gmail.com', 'password1', 'Reece', 'Tang')


def test_short_pass():
    with pytest.raises(InputError):
        result1 = auth_register('John.smith@gmail.com', '12345','John', 'Smithh')
    

def test_short_name():
    with pytest.raises(InputError):
        result2 = auth_register('John.smith@gmail.com', 'password1', 'J', 'Smith')


def test_short_last():
    with pytest.raises(InputError):
        result2 = auth_register('John.smith@gmail.com', 'password1', 'John', 'S')

def test_register_double1():
    result1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
   
    with pytest.raises(InputError):
         result2 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
