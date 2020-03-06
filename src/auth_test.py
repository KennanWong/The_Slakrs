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
#assumes that there will be a dictionary that contains all of users account details, i.e their email
#and their password which is checked before a user is able to login (currently in the users_all dict there is 
#no place to log that information
def test_login1():
    result1 = auth.register('abcde@gmail.com', '12345','John', 'Smithh')
    result2 = auth.login('abcde@gmail.com', '12345')
    
    assert result2['u_id'] == result1['u_id']
    assert result2['token'] == result2['token']

def test_invalid_email_login():
    result1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    with pytest.raises(InputError):
        result2 = auth.login('John.smith@com', 'password1')


def test_wrong_email():
    result1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    with pytest.raises(InputError):
        results2 = auth.login('Smith.john@gmail.com', 'password1')
    

def test_wrong_pass():
    result1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    with pytest.raises(InputError):
        result2 = auth.login('John.smith@gmail.com', 'password2')
    


'''
#############################################################
#                   AUTH_LOGOUT                             #      
#############################################################
'''
# assume register and login works
# assume that users_all functions, and is able to generate u_id

def test_logout1():
    result1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    result2 = auth.login('John.smith@gmail.com', 'password1')
    user1_tk = result2['token']
    assert auth.logout(user1_tk)['is_success'] == True
    

def test_bad_token():
    result1 = auth.register('John.smith@gmail.com', 'password1','John', 'Smithh')
    result2 = auth.login('John.smith@gmail.com', 'password1')
    user1_tk = result2['token']
    
    assert auth.logout('54321')['is_success'] == False




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








