from data_stores import *
from helper_functions import *
from error import InputError, AccessError

def channel_details(tokne, channels_id):
    auth_store = get_auth_data_store
    channel_store = get_channel_data_store

    is_valid_user_id(u_id)
    owner_members = []
    all_members = []

    # Check if channel exists using helper function
    channel = get_channel(channel_id)
    
    # InputError when we try to get details of an invalid channelID
    if channel is None:
        raise InputError(description='Invalid channel_id')

    # Get details of owners and members in the channel
    if u_id in channel['members']:
        name = channel['name']
        for owners in channel['owner_members']:
            owner_members_details = user_details(owners)
            owner_members.append(owners_members_details)
        for members in channel['all_members']:
            all_members_details = user_details(members)
            all_members.append(all_members_details)
        return {
            "name": channel['name'], 
            "owner_members": channel['owner_members'], 
            "all_members": channel['all_members']
        }
    # AccessError when authorised user is not a member of the channel
    else:
        raise AccessError(description = 'Authorised user is not a member of the channel')
