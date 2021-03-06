'''

This file contains all 'message_' functions

'''
from datetime import datetime, timezone             #pylint: disable=W0611
import threading
import hangman
from data_stores import get_messages_store, save_messages_store
from data_stores import save_channel_store
from error import InputError, AccessError
from helper_functions import create_message, get_channel, test_in_channel
from helper_functions import get_user_from, find_message, check_owner, append_later


REACT_IDS = [1]

#pylint compliant
#############################################################
#                   MESSAGE_SEND                            #
#############################################################
def send(payload):
    '''
    function to take a payload, create a new mesaage, fill
    in the parameters and append it to the channels messages
    store as well as the gloabal message_store
    '''
    user = get_user_from('token', payload['token'])
    channel = get_channel(payload['channel_id'])
    if not test_in_channel(user['u_id'], channel):
        raise AccessError(description='User is not in channel')

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

    channel['messages'].append(new_message)

    if txt == '/hangman':
        if not channel['hangman_active']:
            hangman.start(channel)
            channel['hangman_active'] = True
        else:
            hangman.message(channel, 'There is already an active game running')
            hangman.message(channel, hangman.display_hangman())

    if txt.split()[0] == '/guess':
        if not channel['hangman_active']:
            hangman.message(channel, 'There is not a current game of hangman running.\n'+
                            r'If you would like to start one, type \hangman into the chat')
        else:
            if len(txt.split()) == 2:
                new_guess = txt.split()[1]
                if new_guess in r'!@#$%^&*()_+-=[]\;<>?/~`:':
                    hangman.message(channel, 'Invalid guess, guess again')
                else:
                    hangman.guess(channel, new_guess)
            else:
                hangman.message(channel, 'Invalid guess, guess again')

    # append it to the messages_store
    messages = get_messages_store()
    messages.append(new_message)
    save_messages_store()

    # append it to the channels file
    save_channel_store()

    return new_message

#############################################################
#                  MESSAGE_SENDLATER                        #
#############################################################
def sendlater(payload):
    '''
    Function to create a message and have it be sent at a
    '''

    user = get_user_from('token', payload['token'])
    channel = get_channel(payload['channel_id'])
    messages = get_messages_store()
    if not test_in_channel(user['u_id'], channel):
        raise InputError(description='User is not in channel')

    # create a message data type, and fill in details
    # then append to the channels list of messages
    txt = payload['message']
    if len(txt) > 1000:
        raise InputError(description='Message is more than 1000 characters')

    # create the message dictionary
    time = payload['time_sent']

    print(type(time))

    if time < int(datetime.now().timestamp()):
        raise InputError(description='Unable to send as '+
                         'time sent is a time in the past')

    new_message = create_message()
    new_message['time_created'] = time
    new_message['u_id'] = user['u_id']
    new_message['message'] = txt
    new_message['channel_id'] = payload['channel_id']

    # append it to the messages_store first
    messages.append(new_message)
    save_messages_store()

    interval = (time - datetime.now().timestamp())

    # append to the channel message store at a later time
    timer = threading.Timer(interval, append_later, args=[new_message['message_id']])

    timer.start()


    # debugging purposes
    for msg in channel['messages']:
        print(msg['message'])

    return new_message['message_id']

#############################################################
#                   MESSAGE_REMOVE                          #
#############################################################
def remove(payload):  # pylint: disable=R1711
    '''
    Function to remove a message from a channel
    '''
    user = get_user_from('token', payload['token'])
    messages = get_messages_store()

    message = find_message(payload['message_id'])

    channel = get_channel(message['channel_id'])

    if message['u_id'] != user['u_id']:
        if not check_owner(user, channel):
            raise AccessError(description='You do not have permission')

    messages.remove(message)
    channel['messages'].remove(message)

    return

#############################################################
#                   MESSAGE_PIN                             #
#############################################################
def pin(payload): # pylint: disable=R1711
    'testing functionability for message pin'
    user = get_user_from('token', payload['token'])
    message = find_message(payload['message_id'])
    channel = get_channel(message['channel_id'])

    if message['is_pinned'] is True:
        raise InputError(description='Message is already pinned')

    if not test_in_channel(user['u_id'], channel):
        raise AccessError(description='You do not have permission to pin this message')

    if not check_owner(user, channel):
        raise InputError(description='You do not have permission')

    message['is_pinned'] = True

    return

#############################################################
#                   MESSAGE_UNPIN                           #
#############################################################
def unpin(payload): # pylint: disable=R1711
    'testing functionability for message unpin'

    user = get_user_from('token', payload['token'])
    message = find_message(payload['message_id'])

    channel = get_channel(message['channel_id'])

    if message['is_pinned'] is False:
        raise InputError(description='Message is already unpinned')

    if not test_in_channel(user['u_id'], channel):
        raise AccessError(description='You do not have permission to unpin this message')

    if not check_owner(user, channel):
        raise InputError(description='You do not have permission')

    message['is_pinned'] = False

    return


#############################################################
#                   MESSAGE_EDIT                            #
#############################################################
def edit(payload):
    '''
    Function to remove a message from a channel
    '''
    message_store = get_messages_store()
    user = get_user_from('token', payload['token'])
    message = find_message(payload['message_id'])

    channel = get_channel(message['channel_id'])

    if message['u_id'] != user['u_id']:
        if not check_owner(user, channel):
            raise AccessError(description='You do not have permission')

    if len(payload['message']) == 0:  # pylint: disable=C1801, R1705
        channel['messages'].remove(message)
        message_store.remove(message)
        return
    else:
        message['message'] = payload['message']
        return


#############################################################
#                   MESSAGE_REACT                           #
#############################################################
def react(payload):
    '''
    Function to add a react to a given message
    '''
    global REACT_IDS    # pylint: disable=W0603
    user = get_user_from('token', payload['token'])

    message = find_message(int(payload['message_id']))

    channel = get_channel(message['channel_id'])

    if int(payload['react_id']) not in REACT_IDS:
        raise InputError(description='Unable to react with react_id '+
                         str(payload['react_id']))

    if not test_in_channel(user['u_id'], channel):
        raise InputError(description='Unable to react as you are '+
                         'not a part of that channel')

    for i in message['reacts']:
        if i['react_id'] == payload['react_id']:
            # this react is already present in the message
            # just add another u_id
            if user['u_id'] in i['u_ids']:
                # if the user has reacted, unreact them
                unreact(payload)
            i['u_ids'].append(user['u_id'])
            return

    # no previous react wih react_id
    new_react = {
        'react_id' : payload['react_id'],
        'u_ids' : [],
        'is_user_reacted' : False
    }
    new_react['u_ids'].append(user['u_id'])
    message['reacts'].append(new_react)

    return



#############################################################
#                   MESSAGE_UNREACT                         #
#############################################################
def unreact(payload):
    '''
    Function to remove a react from a message
    '''
    global REACT_IDS  # pylint: disable=W0603
    user = get_user_from('token', payload['token'])

    message = find_message(payload['message_id'])

    channel = get_channel(message['channel_id'])

    if int(payload['react_id']) not in REACT_IDS:
        raise InputError(description='Unable to react with react_id '+
                         str(payload['react_id']))

    if not test_in_channel(user['u_id'], channel):
        raise InputError(description='Unable to react as you are '+
                         'not a part of that channel')

    for i in message['reacts']:
        if i['react_id'] == payload['react_id']:
            # this react is already present in the message
            # just remove u_id
            if user['u_id'] not in i['u_ids']:
                raise InputError(description='Attempting to uncreact '+
                                 'a message you have not reacted to')
            i['u_ids'].remove(user['u_id'])
            if len(i['u_ids']) == 0:  # pylint: disable=C1801
                # no one else has reacted, so remove react
                message['reacts'].remove(i)
                print(message['reacts'])
            return

    # unable to find react of react_id in messages
    raise InputError(description='Message with ID message_id ' +
                     'does not contain an active react with with ID react_id')
