'''
This file contains all function stubs for 'other_' functions and misclaneous
'''
import re
from data_stores import reset_auth_store, reset_channel_data_store
from data_stores import get_auth_data_store, get_channel_data_store
from data_stores import reset_messages_store
from helper_functions import reset_message_count, get_user_token
from helper_functions import test_in_channel, validate_uid
from helper_functions import get_user_uid
from error import AccessError, InputError

#############################################################
#                        WORKSPACE_RESET                    #
#############################################################


def workspace_reset():
    '''
    Function to reset the workspace
    '''
    reset_auth_store()
    reset_channel_data_store()
    reset_message_count()
    reset_messages_store()
    return
    
#############################################################
#                        USERS_ALL                          #
#############################################################  

def users_all(payload):

    '''
    Returns a list of all users and their associated details
    '''
    checker = get_user_token(payload['token'])
    
    user_store = get_auth_data_store()
    
    ret = []
    
    user_data = {}

    for i in user_store:
        user_data = {
            'u_id': i['u_id'],
            'email': i['email'],
            'name_first': i['name_first'],
            'name_last': i['name_last'],
            'handle_str': i['handle_str'],
        }
        ret.append(user_data)
    
    return ret 

#############################################################
#                          SEARCH                           #
#############################################################
  
def search(payload):

    '''
    Given a query string, return a collection of 
    messages in all of the channels that the user
    has joined that match the query. Results are
    sorted from most recent message to least recent message
    '''
    
    channel_store = get_channel_data_store()
    returnMessage = []
    
    user = get_user_token(payload['token'])
    
    query_str = payload['query_str']
    
    # if the query is nothing
    if query_str == '':
        return []
                        
    for channel in channel_store:
        if test_in_channel(user['u_id'], channel):
            for msg in channel['messages']:
                if re.search(payload['query_str'], msg['message']):
                    result = {
                        'message_id': msg['message_id'],
                        'u_id': msg['u_id'],
                        'message': msg['message'],
                        'time_created': msg['time_created'].strftime("%H:%M:%S"),
                        'reacts': msg['reacts'],
                        'is_pinned': msg['is_pinned']
                    }
                    returnMessage.append(result)
        
    return returnMessage
    
    
#############################################################
#              ADMIN_USERPERMISSION_CHANGE                  #
############################################################# 


def user_permission_change(payload):

    #what does it mean for permision id to not refer to permission id?
    '''
    changes the permision of a authorised uid
    '''
    if validate_uid(payload['u_id'] is False):
        raise InputError (description='Invalid u_id')

    owner = get_user_token(payload['token'])
    
    chan_user = get_user_uid(payload['u_id'])
    
    if owner['slacker_owner'] is True:
        chan_user['permission_id'] = payload['permission_id']
        return {}
        
    raise AccessError(description='The authorised user is not an owner')
