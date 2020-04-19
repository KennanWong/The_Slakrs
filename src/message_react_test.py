'''
Pytest file to test functionality of message_react
'''

import pytest

import message
from other import workspace_reset
from test_helper_functions import reg_user2, invite_to_ch1
from test_helper_functions import create_ch1, reg_user1, send_msg1
from helper_functions import find_message
from error import InputError


#############################################################
#                   MESSAGE_REACT                           #
#############################################################

def test_react1():
    '''
    Test a valid use of react on your own message
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

    # find the reacts in the message with react_id 1
    # Assert user1 has reacted
    message.react(payload)
    message1_reacts = find_message(msg1['message_id'])['reacts']
    for i in message1_reacts:
        if i['react_id'] == 1:
            assert user1['u_id'] in i['u_ids']


def test_react2():
    '''
    Test a valid use of react where someone else reacts to someones
    elses message
    '''
    workspace_reset()

    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    invite_to_ch1(user1, user2, channel1)

    payload = {
        'token':user2['token'],
        'message_id':msg1['message_id'],
        'react_id': 1
    }
    message.react(payload)
    message1_reacts = find_message(msg1['message_id'])['reacts']
    for i in message1_reacts:
        if i['react_id'] == 1:
            assert user2['u_id'] in i['u_ids']

def test_invalid_msg_id():
    '''
    Test reacting with an invalid message id
    '''
    workspace_reset()
    user1 = reg_user1()


    payload = {
        'token':user1['token'],
        'message_id':1,
        'react_id': 1
    }

    with pytest.raises(InputError):
        message.react(payload)

def test_invalid_react_id():
    '''
    Test a user reacting with an invalid reactId
    '''

    workspace_reset()
    user1 = reg_user1()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    payload = {
        'token':user1['token'],
        'message_id':msg1['message_id'],
        'react_id': 2
    }
    with pytest.raises(InputError):
        message.react(payload)

def test_not_in_channel():
    '''
    Test a user reacting to a message in a channel they
    are not a part of
    '''
    workspace_reset()
    user1 = reg_user1()
    user2 = reg_user2()
    channel1 = create_ch1(user1)
    msg1 = send_msg1(user1, channel1)

    payload = {
        'token':user2['token'],
        'message_id':msg1['message_id'],
        'react_id': 1
    }
    with pytest.raises(InputError):
        message.react(payload)
