from auth import *
import user
import pytest
import other
from error import InputError

'''
#############################################################
#                   AUTH_LOGIN                              #      
#############################################################
'''

def test_login1():
    
    result1 = auth_register('abcde@gmail.com', '12345','John', 'Smithh')
    result2 = auth_login('abcde@gmail.com', '12345')
    
    assert result2['u_id'] == result1['u_id']

def test_invalid_email_login():
    result1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    with pytest.raises(InputError):
        result2 = auth_login('John.smith@com', 'password1')


def test_wrong_email():
    result1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    with pytest.raises(InputError):
        results2 = auth_login('Smith.john@gmail.com', 'password1')
    

def test_wrong_pass():
    result1 = auth_register('John.smith@gmail.com', 'password1','John', 'Smithh')
    with pytest.raises(InputError):
        result2 = auth_login('John.smith@gmail.com', 'password2')



