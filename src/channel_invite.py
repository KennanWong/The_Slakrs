from data_stores import *
from helper_functions import *
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    auth_store = get_auth_data_store
    
    # User ID of person inviting
    user_id_inviter = user_id_from_token(token)

    # Check if channel exists using helper function
    channel = get_channel(channel_id)
    
    # Check if userID is valid, InputError if not
    if not is_valid_user_id(u_id):
        raise InputError(description='Invalid user_id')

    # InputError if channel_id does not refer to a valid channel
    if channel is None:
        raise InputError(description='Invalid channel_id')

    # Check if u_id is already in channel, InputError if not
    if u_id in channel['members']:
        raise InputError(description='User is already a part of the channel')

    # Check if authorised user is a member of the channel, AccessError if not
    if user_id_inviter not in channel['members']:
        raise AccessError(description='Authorised user is not a member of the channel')

    # User is added
    channel['members'].append(u_id)

    print(channel['members'])

    return {}
