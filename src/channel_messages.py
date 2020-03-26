from data_stores import *
from helper_functions import *
from error import InputError, AccessError

def channel_messages(token, channel_id, start):
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
    
    if start < len(channel['messages']):
        if len(channel['messages'][start:]) > 50:
            end = start + 50
            return {
                "messages": #message_list,
                "start": start,
                "end": 
            }
        else:
            end = -1
            #message_list = get the messages
            return {
                "messages": #message_list,
                "start": start,
                "end": -1
            }       
