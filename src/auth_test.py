import auth
import pytest
from error import InputError

'''
#############################################################
#                   AUTH_LOGIN                              #      
#############################################################
'''
#assume register works
#asumme users_all works and we are able to check emails of existing users
#assumes that a check is in place to see if an email is valid or not
def test_login1():
    result1 = auth.register('abcde@gmail.com', '12345','John', 'Smithh')
    result2 = auth.login('abcde@gmail.com', '12345')
    
    assert result2['u_id'] == result1['u_id']
    assert result2['token'] == result2['token']

def test_invalid_email_login():
    with pytest.raises(InputError):
        result1 = auth.register('John.smith@com', 'password1', 'John', 'Smith')


def test_wrong_email():
    with pytest.raises(InputError):
        results1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    

def test_wrong_pass():
    pass


'''
#############################################################
#                   AUTH_LOGOUT                             #      
#############################################################
'''
# assume register and login works
# assume that users_all functions, and is able to generate u_id
def test_logout1():
    assert auth.logout("12345")['is_success'] == True
    

def test_bad_token():
    with pytest.raises(InputError):
        result1 = auth.logout("54321")['is_success']
    pass



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
    result1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    result2 = {'u_id':1, 'token':12345}
    assert result1['u_id'] == result2['u_id']
    

def test_invalid_email_reg():
    with pytest.raises(InputError):
        result1 = auth.register('John.smith@com', 'password1', 'John', 'Smith')

def test_email_used():
    result1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    with pytest.raises(InputError):
        result2 = auth.register('John.smith@gmail.com', 'password1', 'Reece', 'Tang')


def test_short_pass():
    with pytest.raises(InputError):
        result1 = auth.register('John.smith@gmail.com', '12345','John', 'Smithh')
    

def test_short_name():
    with pytest.raises(InputError):
        result2 = auth.register('John.smith@gmail.com', 'password1', 'J', 'Smith')


def test_short_last():
    with pytest.raises(InputError):
        result2 = auth.register('John.smith@gmail.com', 'password1', 'John', 'S')

def test_register_double1():
    result1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
   
    with pytest.raises(InputError):
         result2 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')








