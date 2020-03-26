# This file contains the implementation of all 'user_' functions for the
# server

from error import InputError
from helper_functions import get_user_token, validate_ui
from data_stores import get_channel_data_store, get_data

#############################################################
#                      USER_PROFILE                         #      
#############################################################

def profile(payload):

    '''
    For a valid user, returns information about their user id, 
    email, first name, last name, and handle
    '''
    
    #for invalid u_id given
    if validate_uid(payload['u_id']) == False:
        raise InputError (description='Invalid u_id')

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
    
    if len(payload['name_first']) > 50:
        raise InputError (description='Invalid name_first, above the range of 50 characters')
    if len(payload['name_last']) > 50:
        raise InputError (description='Invalid name_last, above the range of 50 characters')    
    
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
    user = get_user_token(token)
    
    
    
    
    
      
