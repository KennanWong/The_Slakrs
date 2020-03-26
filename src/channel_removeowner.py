from data_stores import *
from helper_functions import *
from error import InputError, AccessError

def channel_removeowner(token, channel_id, u_id):
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store
    
    user_id_remover = user_id_from_token(token)

    # Check if channel exists using helper function
    channel = get_channel(channel_id)
    
    # InputError if channel_id does not refer to a valid channel
    if channel is None:
        raise InputError(description='Invalid channel_id')

    # InputError when user with user id u_id is not an owner of the channel
    if user_id_remover not in channel['owner_members']:
        raise InputError(description='Cannot remove if user is not an owner of the channel')
    
    ###USER REMOVING THEMSELF
    if (len(channel['owner_members']) == 1 and )

    # AccessError when the authorised user is not an owner of the slackr, or an owner of this channel
    # Can't remove someone if you're not owner yourself
    if u_id in channel['owner_members']:
        raise AccessError(description='User is not an owner of the slackr, or an owner of this channel')
    # Otherwise user is removed if they're an owner
    else:
        channel['owner_members'].remove(u_id)
        return {}