'''
Pytest file to test functionality of message_react
'''

import pytest

# import channel
import message
from other import workspace_reset
from test_helper_functions import reg_user2
from test_helper_functions import create_ch1, reg_user1, send_msg1
from test_helper_functions import react_to_msg, invite_to_ch1
from helper_functions import find_message
from error import InputError

#############################################################
#                   MESSAGE_UNREACT                         #
#############################################################

def test_unreact1():
    '''
    Test a valid case of message_unreact to a message they had sent
    '''
    workspace_reset()
    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    # react to the message
    react_to_msg(1, msg1, user1)

    payload = {
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'react_id': 1
    }
    message.unreact(payload)

    message1_reacts = find_message(msg1['message_id'])['reacts']
    for i in message1_reacts:
        if i['react_id'] == 1:
            assert user1['u_id'] not in i['u_ids']


def test_unreact():
    '''
    Test a valid case of message_unreact to a message someone
    else had sent
    '''
    workspace_reset()
    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    invite_to_ch1(user1, user2, channel1)
    msg1 = send_msg1(user1, channel1)

    # react to the message
    react_to_msg(1, msg1, user2)

    payload = {
        'token': user2['token'],
        'message_id': msg1['message_id'],
        'react_id': 1
    }
    message.unreact(payload)

    message1_reacts = find_message(msg1['message_id'])['reacts']
    for i in message1_reacts:
        if i['react_id'] == 1:
            assert user2['u_id'] not in i['u_ids']


def test_not_reacted():
    '''
    Test unreacting to a message they have already reacted to
    '''
    workspace_reset()
    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    payload = {
        'token':user1['token'],
        'message_id':msg1['message_id'],
        'react_id': 1
    }

    with pytest.raises(InputError):
        message.unreact(payload)


def test_invalid_msg_id():
    '''
    Test unreacting with an invalid message id
    '''
    workspace_reset()
    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)
    react_to_msg(1, msg1, user1)


    payload = {
        'token':user1['token'],
        'message_id':2,
        'react_id': 1
    }

    with pytest.raises(InputError):
        message.unreact(payload)

def test_invalid_react_id():
    '''
    Test a user unreacting with an invalid reactId
    '''
    workspace_reset()
    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)
    react_to_msg(1, msg1, user1)

    payload = {
        'token':user1['token'],
        'message_id':msg1['message_id'],
        'react_id': 2
    }
    with pytest.raises(InputError):
        message.unreact(payload)

def test_not_in_channel():
    '''
    Test a user unreacting to a message in a channel they
    are not a part of
    '''
    workspace_reset()
    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)
    react_to_msg(1, msg1, user1)

    payload = {
        'token':user2['token'],
        'message_id':msg1['message_id'],
        'react_id': 1
    }
    with pytest.raises(InputError):
        message.unreact(payload)
