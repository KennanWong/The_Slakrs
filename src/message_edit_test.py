'''
Pytest file to test functionality of message_remove
'''

import pytest

import message
# import channel
import channels
from other import workspace_reset
from test_helper_functions import reg_user2, register_and_create, send_msg1
from data_stores import get_messages_store
from error import AccessError




#############################################################
#                   MESSAGE_EDIT                            #
#############################################################


def test_edit1():
    '''
    Test valid use of message.edit where someone is editing their
    own message
    '''
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    msg1 = send_msg1(user1, channel1)

    message.edit({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'message': 'edit'
    })

    assert msg1['message'] == 'edit'

'''
def test_edit2():
    
    Test if an owner is editing another users message
    
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()

    channel.invite({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user2['u_id']
    })

    msg1 = send_msg1(user2, channel1)

    message.edit({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'message': 'edit'
    })

    assert msg1['message'] == 'edit'
'''


def test_edit3():
    '''
    Someone attempts to edit a message by replacing it witha a blank string
    '''
    workspace_reset()

    message_store = get_messages_store()

    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    msg1 = send_msg1(user1, channel1)

    message.edit({
        'token': user1['token'],
        'message_id': msg1['message_id'],
        'message': ''
    })

    assert msg1 not in message_store
    assert msg1 not in channel1['messages']

'''
def test_unauth_edit1():
    # Someone is attempting to edit another users message but they are not an
    # owner
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()

    channel.invite({
        'token': user1['token'],
        'channel_id': channel1['channel_id'],
        'u_id': user2['u_id']
    })

    msg1 = send_msg1(user1, channel1)
    
    with pytest.raises(AccessError):
        message.edit({
            'token': user2['token'],
            'message_id': msg1['message_id'],
            'message': 'edit'
        })
'''

def test_unauth_edit2():
    '''
    Someone attempting to edit a message in a channel they are not a part of
    '''
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()

    msg1 = send_msg1(user1, channel1)

    with pytest.raises(AccessError):
        message.edit({
            'token': user2['token'],
            'message_id': msg1['message_id'],
            'message': 'edit'
        })
