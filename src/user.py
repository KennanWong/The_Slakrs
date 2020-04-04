# This file contains the implementation of all 'user_' functions for the
# server

from error import InputError
from helper_functions import get_user_token, validate_uid, test_email
from helper_functions import check_used_email, check_used_handle

#############################################################
#                      USER_PROFILE                         #      
#############################################################

def profile(payload):
    '''
    For a valid user, returns information about their user id, 
    email, first name, last name, and handle
    '''
    
    if validate_uid(payload['u_id']) is False:
        raise InputError(description='Invalid u_id')

    user = get_user_token(payload['token'])
    #returns user information
    #user_two = getUserById(u_id)
        
    return ({
        'u_id' : user['u_id'],
        'email' : user['email'],
        'name_first' : user['name_first'],
        'name_last' : user['name_last'],
        'handle_str' : user['handle_str'],
    })


#############################################################
#                   USER_PROFILE_SETNAME                    #
#############################################################

def profile_setname(payload):
    
    '''
    Update the authorised user's first and last name
    '''
    user = get_user_token(payload['token'])
    
    if not (1 < len(payload['name_first']) < 50):
        raise InputError(description='Invalid name_first, above the range of 50 characters')
    if not (1 < len(payload['name_last']) < 50):
        raise InputError(description='Invalid name_last, above the range of 50 characters')    
    
    user['name_first'] = payload['name_first']
    user['name_last'] = payload['name_last']
    return ({})
    
#############################################################
#                   USER_PROFILE_SETEMAIL                   #
#############################################################

def profile_setemail(payload):
    '''
    Update the authorised user's email address
    '''
    
    #test email is valid and not been used before
    new_email = test_email(payload['email'])
    assert check_used_email(new_email) == 1
    
    user = get_user_token(payload['token'])
    user['email'] = new_email
    return {}
    
#############################################################
#                   USER_PROFILE_SETHANDLE                  #
#############################################################

def profile_sethandle(payload):
    
    '''
    Update the authorised user's handle (i.e. display name)
    '''
    #test handle is valid and not been used before
    if len(payload['handle_str']) < 3 or len(payload['handle_str']) > 20:
        raise InputError(description='handle_str should be between 3-20 characters')
    
    assert check_used_handle(payload['handle_str']) == 1
    
    user = get_user_token(payload['token'])
    user['handle_str'] = payload['handle_str']
    return {}
    
