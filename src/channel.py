'This file contains all channel functions'

from data_stores import get_auth_data_store, get_channel_data_store
from helper_functions import user_id_from_token, get_channel, test_in_channel
from helper_functions import user_details, is_valid_user_id, get_user_token
from helper_functions import check_owner
from error import InputError, AccessError

# pylint: disable=W0612
# pylint: disable=C1801
# pylint: disable=C0301
# pylint: disable=R0912
# pylint: disable=R1705
# pylint: disable=R1710

#pylint compliant

#############################################################
#                  CHANNEL_INVITE                           #
#############################################################
def invite(token, channel_id, u_id):
    'This is the function for channel_invite'
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
    if test_in_channel(int(u_id), channel):
        raise InputError(description='User is already a part of the channel')

    # Check if authorised user is a member of the channel, AccessError if not
    if not test_in_channel(user_id_inviter, channel):
        raise AccessError(description='Authorised user is not a member of the channel')

    # User is added
    new_user = user_details(u_id)
    channel['members'].append(new_user)

    return {}


#############################################################
#                  CHANNEL_DETAILS                          #
#############################################################

def details(token, channel_id):
    'This is the function for channel_details'
    user = get_user_token(token)
    u_id1 = user['u_id']

    owner_members = []
    all_members = []

    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # If the channel is public, safe to display details
    # If not then raise error
    if test_in_channel(u_id1, channel):
        for owner in channel['owners']:
            owner_dets = user_details(owner)
            owner_members.append(user_details(owner_dets))
            all_members.append(user_details(owner_dets))
        for member in channel['members']:
            member_dets = user_details(member)
            all_members.append(user_details(member_dets))
        return {
            #ret_package = {
            "name": channel['name'],
            "owner_members": owner_members,
            "all_members": all_members
        }
    else:
        raise AccessError(description='Authorised user is not a member of the channel')

    # Get details of owners and members in the channel
    #if channel['is_public']:
    #    return ret_package
        #name = channel['name']

    # AccessError when authorised user is not a member of the channel
    #if test_in_channel(u_id1, channel):
    #    return ret_package

#############################################################
#                  CHANNEL_MESSAGES                         #
#############################################################
def messages(token, channel_id, start):
    'This is the function for channel_messages'
    auth_store = get_auth_data_store

    u_id = user_id_from_token(token)
    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # Check if authorised user is a member of the channel, AccessError if not
    if not test_in_channel(u_id, channel):
        raise AccessError(description='Authorised user is not a member of the channel')

    # InputError if start is not of type int
    if not isinstance(start, int):
        raise InputError(description='Start is not of type integer')

    # InputError when start is greater than or equal to the total number of messages in the channel
    if start > len(channel['messages']):
        raise InputError(description='Start is greater than or equal to the total number of messages in the channel')

    # Incorrect indexing
    if start < 0:
        raise InputError(description='Incorrect indexing')

    # When there are 0 messages
    if (len(channel['messages'])) == 0:
        return {
            "messages": [],
            "start": start,
            "end": -1
        }

    messages_list = []
    messages_dict = {}
    if start + 50 > len(channel['messages']):
        interval = start + 50
    else:
        interval = len(channel['messages'])
    for msgs in channel['messages'][start: interval]:
        messages_dict = {
            'message_id': msgs['message_id'],
            'u_id': msgs['u_id'],
            'message': msgs['message'],
            'time_created': msgs['time_created'],
            'reacts': msgs['reacts'],
            'is_pinned': msgs['is_pinned']
        }
        for reacts in msgs['reacts']:
            for users_reacted in reacts['u_ids']:
                if u_id in reacts['u_ids']:
                    reacts['is_user_reacted'] = True
        messages_list.append(messages_dict)

    messages_list.reverse()

    if start < len(channel['messages']):
        if len(channel['messages'][start:]) > 50:
            end = start + 50
            return {
                "messages": messages_list,
                "start": start,
                "end": end
            }
        if len(channel['messages'][start:]) < 50:
            return {
                "messages": messages_list,
                "start": start,
                "end": -1
            }


#############################################################
#                     CHANNEL_LEAVE                         #
#############################################################
def leave(token, channel_id):
    'This is the function for channel_leave'
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store

    user = get_user_token(token)
    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # Check if authorised user is a member of the channel, AccessError if not
    if not test_in_channel(user['u_id'], channel):
        raise AccessError(description='Cannot leave channel when user is not a member in the first place')

    # User leaving channel
    user_det = user_details(user['u_id'])
    print(user_det)
    print(channel['owners'])
    if user_det in channel['owners']:
        channel['owners'].remove(user_det)

    print(channel['members'])
    if user_det in channel['members']:
        channel['members'].remove(user_det)

    return {}


#############################################################
#                     CHANNEL_JOIN                          #
#############################################################
def join(token, channel_id):
    'This is the function for channel_join'
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store

    user = get_user_token(token)

    user_dets = {
        'u_id' : user['u_id'],
        'name_first': user['name_first'],
        'name_last': user['name_last']
    }
    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # InputError if channel_id does not refer to a valid channel
    if channel is None:
        raise InputError(description='Invalid channel_id')

    #or if not channel['is_public']
    if channel['is_public'] is True and user['permission_id'] == 1:
        channel['owners'].append(user_dets)
    elif channel['is_public'] is True and user['permission_id'] == 2:
        channel['members'].append(user_dets)
    elif channel['is_public'] is False and user['permission_id'] == 1:
        channel['owners'].append(user_dets)
    else:
        # AccessError when attempting to join a private channel
        raise AccessError(description='Cannot join a private channel')

    return {}


#############################################################
#                   CHANNEL_ADDOWNER                        #
#############################################################
def addowner(token, channel_id, u_id):
    'This is the function for channel_addowner'
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store

    channel = get_channel(channel_id)
    user_id_adder = user_id_from_token(token)
    adder_dets = user_details(user_id_adder)
    addee_dets = user_details(u_id)

    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # InputError when user with user id u_id is already an owner of the channel
    if addee_dets in channel['owners']:
        raise InputError(description='Cannot add if user is already an owner of the channel')

    # InputError if user isn't even a member of the channel
    if not test_in_channel(u_id, channel):
        raise InputError(description='User is not a member of channel')

    # AccessError when the authorised user is not an owner of the slackr, or an owner of this
    # channel
    # Can't add someone as an owner if you're not an owner yourself
    if not check_owner(adder_dets, channel):
        raise AccessError(description='User is not an owner of the slackr, or an owner of this channel')
    # Otherwise user is added as an owner
    else:
        channel['owners'].append(addee_dets)
        channel['members'].remove(addee_dets)
        #channel['members'].remove(addee_dets)
        return {}


#############################################################
#                  CHANNEL_REMOVEOWNER                      #
#############################################################
def removeowner(token, channel_id, u_id):
    'This is the function for channel_removeowner'
    auth_store = get_auth_data_store
    channels_store = get_channel_data_store

    user_id_remover = user_id_from_token(token)
    remover_dets = user_details(user_id_remover)

    removee_dets = user_details(u_id)

    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # InputError when user with user id u_id is not an owner of the channel
    if removee_dets not in channel['owners']:
        raise InputError(description='Cannot remove if user is not an owner of the channel')

    # AccessError when the authorised user is not an owner of the slackr, or an owner of this
    # channel
    # Can't remove someone if you're not owner yourself
    print(remover_dets)
    print(channel['owners'])
    if remover_dets not in channel['owners']:
        raise AccessError(description='User is not an owner of the slackr, or an owner of this channel')
    # Otherwise user is removed if they're an owner
    else:
        channel['owners'].remove(removee_dets)
        channel['members'].append(removee_dets)
        return {}
