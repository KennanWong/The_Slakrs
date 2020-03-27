# This file contains the implementation of all 'auth_' functions for the
# server
import datetime
import sched
import threading
from data_stores import get_messages_store
from error import InputError, AccessError
from helper_functions import create_message, get_channel, test_in_channel, get_user_token, find_message, check_owner, append_later, get_message_count


react_ids = [1]

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
#                  MESSAGE_SENDLATER                        #      
#############################################################
def sendlater(payload):
    user = get_user_token(payload['token'])
    channel = get_channel(payload['channel_id'])
    messages = get_messages_store()
    if test_in_channel(user['u_id'], channel) == False:
        raise InputError(description='User is not in channel')

    # create a message data type, and fill in details
    # then append to the channels list of messages
    txt = payload['message']
    if len(txt) > 1000:
        raise InputError(description='Message is more than 1000 characters')

    # create the message dictionary
    time = datetime.datetime.fromtimestamp(payload['time_sent'])

    if time < datetime.datetime.now():
        raise InputError(description='Unable to send as '+
            'Time sent is a time in the past')

    new_message = create_message()
    new_message['time_created'] = time
    new_message['u_id'] = user['u_id']
    new_message['message'] = txt
    new_message['channel_id'] = payload['channel_id']

    # append it to the messages_store first
    messages.append(new_message)

    interval = (time - datetime.datetime.now()).total_seconds()

    # append to the channel message store at a later time
    timer = threading.Timer(interval, append_later, args = [new_message['message_id']])

    timer.start()

    # debugging purposes
    for msg in channel['messages']:
        print(msg['message'])

    return new_message['message_id']

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

#############################################################
#                   MESSAGE_PIN                             #      
#############################################################
def pin(payload):

    channel_store = get_channel_data_store()
    messages = get_messages_store()

    user = get_user_token(payload['token'])
    message = find_message(payload['message_id'])

    channel = get_channel(message['channel_id'])
    

    if message['is_pinned'] is True:
        raise InputError(description='Message is already pinned')

    else:
        if check_owner(user, channel) is True:
            message['is_pinned'] = True
        else:
            raise InputError(description='You do not have permission')

    return
    
#############################################################
#                   MESSAGE_EDIT                            #      
#############################################################
def edit(payload):
    
    user = get_user_token(payload['token'])
    message = find_message(payload['message_id'])

    channel = get_channel(message['channel_id'])

    if message['u_id'] != user['u_id']:
        if check_owner(user, channel) == False:
            raise AccessError(description='You do not have permission')

    message['message'] = payload['message']

    return
    

#############################################################
#                   MESSAGE_UNPIN                           #      
#############################################################
def unpin(payload):

    channel_store = get_channel_data_store()
    messages = get_messages_store()

    user = get_user_token(payload['token'])
    message = find_message(payload['message_id'])

    channel = get_channel(message['channel_id'])
    
    if message['is_pinned'] is False:
        raise InputError(description='Message is already unpinned')

    else:
        if check_owner(user, channel) is True:
            message['is_pinned'] = False
        else:
            raise InputError(description='You do not have permission')

    
    return


#############################################################
#                   MESSAGE_REACT                           #      
#############################################################
def react(payload):
    global react_ids
    user = get_user_token(payload['token'])

    message = find_message(int(payload['message_id']))

    channel = get_channel(message['channel_id'])

    if (int(payload['react_id']) in react_ids) != True:
        raise InputError(description='Unable to react with react_id '+
        payload['react_id'])
    
    if test_in_channel(user['u_id'], channel) == False:
        raise InputError(description='Unable to react as you are '+
        'not a part of that channel')

    for i in message['reacts']:
        if i['react_id'] == payload['react_id']:
            # this react is already present in the message
            # just add another u_id
            if (user['u_id'] in i['u_ids']):
                raise InputError(description='Already reacted')
            i['u_ids'].append(user['u_id'])
            return
    
    # no previous react wih react_id
    new_react = {
        'react_id' : payload['react_id'],
        'u_ids' : [],
        'is_user_reacted' : ''
    }
    new_react['u_ids'].append(user['u_id'])
    message['reacts'].append(new_react)

    print (message['reacts'])
    return



#############################################################
#                   MESSAGE_UNREACT                         #      
#############################################################
def unreact(payload):
    global react_ids
    user = get_user_token(payload['token'])

    message = find_message(payload['message_id'])

    channel = get_channel(message['channel_id'])

    if (int(payload['react_id']) in react_ids) != True:
        raise InputError(description='Unable to react with react_id '+
        payload['react_id'])

    if test_in_channel(user['u_id'], channel) == False:
        raise InputError(description='Unable to react as you are '+
        'not a part of that channel')

    for i in message['reacts']:
        if i['react_id'] == payload['react_id']:
            # this react is already present in the message
            # just remove u_id
            if (user['u_id'] in i['u_ids']) == False:
                raise InputError(description='Attempting to uncreact '+
                'a message you have not reacted to')
            i['u_ids'].remove(user['u_id'])
            if len(i['u_ids']) == 0:
                # no one else has reacted, so remove react
                message['reacts'].remove(i)
                print (message['reacts'])
            return
    
    # unable to find react of react_id in messages 
    raise InputError(description = 'Message with ID message_id ' +
    'does not contain an active react with with ID react_id')

