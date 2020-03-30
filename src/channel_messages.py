from data_stores import *
from helper_functions import *
from error import InputError, AccessError

def channel_messages(token, channel_id, start):
    auth_store = get_auth_data_store

    u_id = user_id_from_token(token)
    # Check if channel exists using helper function
    channel = get_channel(channel_id)

    # InputError when we try to get details of an invalid channelID
    #if channel is None:
    #    raise InputError(description='Invalid channel_id')

    # Check if authorised user is a member of the channel, AccessError if not
    if not test_in_channel(u_id, channel):
        raise AccessError(description='Authorised user is not a member of the channel')
      
    # InputError when start is greater than or equal to the total number of messages in the channel
    if start >= len(channel['messages']):
        raise InputError(description='Start is greater than or equal to the total number of messages in the channel')
    
    # Incorrect indexing
    if start < 0 or start > len(channel['messages']):
        raise InputError(description='Incorrect indexing')
    
    if not isinstance(start, int):
        raise InputError(description='Start is not of type integer')

    # When there are 0 messages
    if (len(channel['messages'])) == 0:
        return {
            "messages": [],
            "start": start,
            "end": start
        }
    
    messages_list = []
    messages_dict = {}
    if start + 50 > len(channel['messages']):
        interval = start + 50
    else:
        interval = len(channel['messages'])
    for messages in channel['messages'][start: interval]:
        messages_dict = {
            'message_id': messages['message_id'],
            'u_id': messages['u_id'],
            'message': messages['message'],
            'time_created': messages['time_created'],
            'reacts': messages['reacts'],
            'is_pinned': messages['is_pinned']
        }
        for reacts in messages['reacts']:
            for users_reacted in reacts['u_ids']:
                if u_id in reacts['u_id']:
                    reacts['is_this_user_reacted'] == True
        messages_list.append(messages_dict)

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