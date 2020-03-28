from data_stores import *
from helper_functions import *
from error import InputError, AccessError

def channel_join(token, channel_id):
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store

    # Check if channel exists using helper function
    channel = get_channel(channel_id)
    
    if user['slack_owner'] == True:
    # InputError if channel_id does not refer to a valid channel
    if channel is None:
        raise InputError(description='Invalid channel_id')
    
    #or if not channel['is_public']
    if channel['is_public'] == True and user['permission_id'] == 1:
        channel['owner_members'].append(user)
    elif channel['is_public'] == True and user['permission_id'] == 2:
        channel['all_members'].append(user)
    elif channel['is_public'] == False and user['permission_id'] == 1:
        channel['owner_members'].append(user)
    else:
        # AccessError when attempting to join a private channel
        raise AccessError(description='Cannot join a private channel')

    return {}
