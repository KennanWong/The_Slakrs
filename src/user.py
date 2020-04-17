# This file contains the implementation of all 'user_' functions for the
# server

from error import InputError, AccessError
from data_stores import get_channel_data_store
from channel import addowner, removeowner
from helper_functions import get_user_from, validate_uid, test_email, get_user_token
from helper_functions import test_in_channel, check_channel_permission
from helper_functions import check_used_email, check_used_handle, get_user_from

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

    user = get_user_from('token', payload['token'])
    #returns user information
    
    user2 = get_user_from('u_id', int(payload['u_id']))


    return ({
        'u_id' : user2['u_id'],
        'email' : user2['email'],
        'name_first' : user2['name_first'],
        'name_last' : user2['name_last'],
        'handle_str' : user2['handle_str'],
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
    
#############################################################
#              ADMIN_USERPERMISSION_CHANGE                  #
############################################################# 


def permission_change(payload):

    #what does it mean for permision id to not refer to permission id?
    '''
    changes the permision of a authorised uid
    We must also update their permissions in all channels they have joined
    '''
    
    if validate_uid(payload['u_id']) is False:
        raise InputError (description='Invalid u_id')

    owner = get_user_token(payload['token'])
    change_user = get_user_from('u_id', payload['u_id'])
    
    if owner['permission_id'] != 1:
        raise AccessError(description='The authorised user is not an owner')

    change_user['permission_id'] = payload['permission_id']
    '''
    Update their permissions in all channels they are apart of
    '''
    '''
    channels_store = get_channel_data_store()
    for channel in channels_store:
        if test_in_channel(change_user['u_id'], channel):
            if payload['permission_id'] == 1:
            # if change permission to 1 --> now an owner in all channels
                current_permission = check_channel_permission(change_user, channel)
                if current_permission == 'member':
                    addowner(owner['token'], channel['channel_id'], change_user['u_id'])
                
            elif payload['permission_id'] ==  2:
            # if change permission to 2 --> now a member in all channels
                removeowner(owner['token'], channel['channel_id'], change_user['u_id'])
    '''
    
    return
        
    
