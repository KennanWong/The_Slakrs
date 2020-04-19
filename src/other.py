'''
This file contains all function stubs for 'other_' functions and misclaneous
'''
import re
from data_stores import reset_auth_store, reset_channel_data_store
from data_stores import get_auth_data_store, get_channel_data_store
from data_stores import reset_messages_store
from helper_functions import reset_message_count, get_user_token
from helper_functions import test_in_channel, validate_uid
from helper_functions import get_user_uid, get_user_from
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
            'profile_img_url': i['profile_img_url']
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
            print("searching in channel: "+ channel['name'])
            for msg in channel['messages']:
                if re.search(payload['query_str'].lower(), msg['message'].lower()):
                    result = {
                        'message_id': msg['message_id'],
                        'u_id': msg['u_id'],
                        'message': msg['message'],
                        'time_created': msg['time_created'],
                        'reacts': msg['reacts'],
                        'is_pinned': msg['is_pinned']
                    }
                    returnMessage.append(result)
    
    print(returnMessage)

    return returnMessage


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
