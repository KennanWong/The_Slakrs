# This file contains the implementation of all 'auth_' functions for the
# server

from data_stores import get_messages_store
from error import InputError, AccessError
from helper_functions import create_message, get_channel, test_in_channel, get_user_token, find_message, check_owner


#############################################################
#                   MESSAGE_SEND                            #      
#############################################################
def send(payload):
    user = get_user_token(payload['token'])
    channel = get_channel(payload['channel_id'])
    if test_in_channel(user['u_id'], channel) == False:
        raise InputError(description='User is not in channel')

    # create a message data type, and fill in details
    # then append to the channels list of messages
    txt = payload['message']
    if len(txt) > 1000:
        raise InputError(description='Message is more than 1000 characters')

    # create the message dictionary
    new_message = create_message()
    new_message['u_id'] = user['u_id']
    new_message['message'] = txt
    new_message['channel_id'] = payload['channel_id']

    # append it to the messages_store
    messages = get_messages_store()
    messages.append(new_message)

    # append it to the channels file
    channel['messages'].append(new_message)

    # debugging purposes
    for msg in channel['messages']:
        print(msg['message'])

    return new_message


#############################################################
#                   MESSAGE_REMOVE                          #      
#############################################################
def remove(payload):
    user = get_user_token(payload['token'])
    messages = get_messages_store()

    message = find_message(payload['message_id'])

    channel = get_channel(message['channel_id'])

    if message['u_id'] != user['u_id']:
        if check_owner(user, channel) == False:
            raise AccessError(description='You do not have permission')
    
    messages.remove(message)
    channel['messages'].remove(message)

    return