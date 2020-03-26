from data_stores import *
from helper_functions import *
from error import InputError, AccessError

def channel_leave(token, channel_id):
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store

    # Check if channel exists using helper function
    channel = get_channel(channel_id)
    
    # InputError if channel_id does not refer to a valid channel
    if channel is None:
        raise InputError(description='Invalid channel_id')

    # Check if authorised user is a member of the channel, AccessError if not
    if u_id not in channel['members']:
        raise AccessError(description='Cannot leave channel when user is not a member in the first place')

    # User leaving channel
    for user in channel['all_members']:
        if user['u_id'] == u_id:
            channel['all_members'].remove(user)
            if owner['u_id'] == u_id:
                channel['owner_members'].remove(user)

    return {}