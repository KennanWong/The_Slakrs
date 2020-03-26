from data_stores import *
from helper_functions import *
from error import InputError, AccessError

def channel_join(token, channel_id):
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store

    # Check if channel exists using helper function
    channel = get_channel(channel_id)
    
    # InputError if channel_id does not refer to a valid channel
    if channel is None:
        raise InputError(description='Invalid channel_id')

    # AccessError when attempting to join a private channel
    if channel['is_public'] == False: #or if not channel['is_public']
        raise AccessError(description='Cannot join a private channel')
    else:
        # User joining channel
        for user in channel['all_members']:
            if user['u_id'] == u_id:
                channel['all_members'].append(user)
    
    return {}
    