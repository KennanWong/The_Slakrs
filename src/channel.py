from data_stores import *
from helper_functions import user_id_from_token, get_channel, test_in_channel
from helper_functions import user_details, is_valid_user_id, get_user_token
from helper_functions import check_owner
from error import InputError, AccessError

#############################################################
#                  CHANNEL_INVITE                           #
#############################################################

def invite(token, channel_id, u_id):
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

    user = get_user_token(token)

    owner_members = []
    all_members = []

    # Check if channel exists using helper function
    channel = get_channel(channel_id)
    
    '''
    You dont need this as get_channel will already check this and raise
    an error
    # InputError when we try to get details of an invalid channelID
    if channel is None:
        raise InputError(description='Invalid channel_id')
    '''
    # Get details of owners and members in the channel
    if test_in_channel(user['u_id'], channel):
        # name = channel['name']
        for owner in channel['owners']:
            owner_members.append(user_details(owner['u_id']))
        for member in channel['members']:
            all_members.append(user_details(member['u_id']))
        return {
            "name": channel['name'], 
            "owner_members": owner_members, 
            "all_members": all_members
        }
    # AccessError when authorised user is not a member of the channel
    else:
        raise AccessError(description = 'Authorised user is not a member of the channel')
    
'''
#############################################################
#                  CHANNEL_MESSAGES                         #
#############################################################
def messages(token, channel_id, start):
    
    auth_store = get_auth_data_store

    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # InputError when we try to get details of an invalid channelID
    if channel is None:
        raise InputError(description='Invalid channel_id')

    # Check if authorised user is a member of the channel, AccessError if not
    if u_id not in channel['members']:
        raise AccessError(description = 'Authorised user is not a member of the channel')
      
    # InputError when start is greater than or equal to the total number of messages in the channel
    if start >= len(messages):
        raise InputError(description='Start is greater than or equal to the total number of messages in the channel')

    if not isinstance(start, int):
        raise InputError(description='Start is not of type integer')

    # When there are 0 messages
    if (len(channel['messages'])) == 0:
        return {
            "messages": [],
            "start": start,
            "end": end
        }
    
    message_list = []
    for messages in channel['messages']:
        for reacts in message['reacts']:
            for users_reacted in react['u_ids']:
                if u_id in reacts['u_id']:
                    reacts['is_this_user_reacted'] == True
                else:
                    reacts['is_this_user_reacted'] == False

    messsage_dict = {
        'message_id': messages['message_id'],
        'u_id': messages['u_id'],
        'message': messages['message'],
        'time_created': messages['time_created'],
        'reacts': messages['reacts'],
        'is_pinned': messages['is_pinned']
    }
    message_list.append(message_dict)

    if start < len(channel['messages']):
        if len(channel['messages'][start:]) > 50:
            end = start + 50
            return {
                "messages": messages_list,
                "start": start,
                "end": end
            }
        else:
            end = -1
            return {
                "messages": messages_list,
                "start": start,
                "end": -1
            }       
'''   
#############################################################
#                     CHANNEL_LEAVE                         #
#############################################################
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


#############################################################
#                   CHANNEL_ADDOWNER                        #
#############################################################
def addowner(token, channel_id, u_id):
    
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
        raise InputError(description='Cannot add if user is already an owner of the channe;')
    
    # InputError if user isn't even a member of the channel
    if not test_in_channel(u_id, channel):   
        raise InputError(description='User is not a member of channel')
    
    # AccessError when the authorised user is not an owner of the slackr, or an owner of this channel
    # Can't add someone as an owner if you're not an owner yourself
    if not check_owner(adder_dets, channel):
        raise AccessError(description='User is not an owner of the slackr, or an owner of this channel')
    # Otherwise user is added as an owner
    else:
        channel['owners'].append(addee_dets)
        channel['members'].remove(addee_dets)
        return {}


#############################################################
#                  CHANNEL_REMOVEOWNER                      #
#############################################################
def removeowner(token, channel_id, u_id):
    
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
    
    ###USER REMOVING THEMSELF
    # if (len(channel['owner_members']) == 1)

    # AccessError when the authorised user is not an owner of the slackr, or an owner of this channel
    # Can't remove someone if you're not owner yourself
    print (remover_dets)
    print (channel['owners'])
    if remover_dets not in channel['owners']:
        raise AccessError(description='User is not an owner of the slackr, or an owner of this channel')
    # Otherwise user is removed if they're an owner
    else:
        channel['owners'].remove(removee_dets)
        channel['members'].append(removee_dets)
        return {}
