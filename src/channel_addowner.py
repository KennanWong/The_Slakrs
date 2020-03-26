from data_stores import *
from helper_functions import *
from error import InputError, AccessError

def channel_addowner(token, channel_id, u_id):
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store
    
    user_id_adder = user_id_from_token(token)

    # Check if channel exists using helper function
    channel = get_channel(channel_id)
    
    # InputError if channel_id does not refer to a valid channel
    if channel is None:
        raise InputError(description='Invalid channel_id')

    # InputError when user with user id u_id is already an owner of the channel
    if user_id_adder in channel['owner_members']:
        raise InputError(description='Cannot add if user is already an owner of the channe;')
    
    # InputError if user isn't even a member of the channel
    if u_id not in channel['all_members']:   
        raise InputError(description='User is not a member of channel')
    
    # AccessError when the authorised user is not an owner of the slackr, or an owner of this channel
    # Can't add someone as an owner if you're not an owner yourself
    if u_id in channel['owner_members']:
        raise AccessError(description='User is not an owner of the slackr, or an owner of this channel')
    # Otherwise user is added as an owner
    else:
        channel['owner_members'].append(u_id)
        return {}