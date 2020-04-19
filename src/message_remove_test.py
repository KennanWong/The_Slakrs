'''
Pytest file to test functionality of message_remove
'''
import pytest

import message
import channel
from other import workspace_reset
from test_helper_functions import reg_user2, register_and_create, send_msg1
from test_helper_functions import invite_to_ch1
from data_stores import get_messages_store
from error import InputError, AccessError


#############################################################
#                   MESSAGE_REMOVE                          #
#############################################################


def test_remove1():
    '''
    Test a valid use of message.remove
    '''
    workspace_reset()
    messages_store = get_messages_store()
    ret = register_and_create()
    user = ret['user']
    channel1 = ret['channel']

    msg1 = send_msg1(user, channel1)

    message.remove({
        'token': user['token'],
        'message_id': msg1['message_id']
    })

    assert msg1 not in messages_store
    assert msg1 not in channel1['messages']


def test_remove2():
    '''
    The admin of a channel is attempting to remove a message
    '''
    workspace_reset()
    messages_store = get_messages_store()


    #register user1 and create channel1
    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()

    channel.invite(user1['token'], channel1['channel_id'], user2['u_id'])

    msg1 = send_msg1(user2, channel1)

    message.remove({
        'token': user1['token'],
        'message_id': msg1['message_id']
    })

    assert msg1 not in messages_store
    assert msg1 not in channel1['messages']


def test_no_msg():
    '''
    Attempting to remove a message that has been already removed or does
    not exist causing an input error
    '''
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']

    with pytest.raises(InputError):
        message.remove({
            'token': user1['token'],
            'message_id': 1
        })


def test_unauth_remove1():
    '''
    Attempting remove another users message in the same channel
    '''
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()
    msg1 = send_msg1(user1, channel1)

    invite_to_ch1(user1, user2, channel1)

    with pytest.raises(AccessError):
        message.remove({
            'token': user2['token'],
            'message_id': msg1['message_id']
        })


def test_unauth_remove2():
    '''
    Attempting remove another users message in a channel
    they are not a part of
    '''
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()

    msg1 = send_msg1(user1, channel1)

    with pytest.raises(AccessError):
        message.remove({
            'token': user2['token'],
            'message_id': msg1['message_id']
        })
