from data_stores import *
from helper_functions import  get_channel, test_in_channel
from helper_functions import get_user_token, user_details
from helper_functions import check_owner
from error import InputError, AccessError

def join(token, channel_id):
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store

    user = get_user_token(token)
    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # InputError if channel_id does not refer to a valid channel
    if channel is None:
        raise InputError(description='Invalid channel_id')
    
    #or if not channel['is_public']
    if channel['is_public'] == True and user['permission_id'] == 1:
        channel['owners'].append(user)
    elif channel['is_public'] == True and user['permission_id'] == 2:
        channel['members'].append(user)
    elif channel['is_public'] == False and user['permission_id'] == 1:
        channel['owners'].append(user)
    else:
        # AccessError when attempting to join a private channel
        raise AccessError(description='Cannot join a private channel')

    return {}

def leave(token, channel_id):
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store

    user =get_user_token(token)
    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # Check if authorised user is a member of the channel, AccessError if not
    if not test_in_channel(user['u_id'], channel):
        raise AccessError(description='Cannot leave channel when user is not a member in the first place')

    # User leaving channel
    user_det = user_details(user['u_id'])

    if user_det in channel['owners']:
        channel['owners'].remove(user_det)
    
    if user_det in channel['members']:
        channel['members'].remove(user_det)
    
    return {}