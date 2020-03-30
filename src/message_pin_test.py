import pytest

import message
import channel
from other import workspace_reset
from test_helper_functions import reg_user1, register_and_create, send_msg1, reg_user2
from error import InputError, AccessError
from data_stores import get_channel_data_store, get_messages_store


#############################################################
#                   MESSAGE_PIN                             #
#############################################################
def test_pin():

    #testing functionability for message pin

    workspace_reset()
    
    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    msg1 = send_msg1(user, channel)

    message.pin({
        'token': user['token'],
        'message_id': msg1['message_id']
    })

    assert msg1['is_pinned'] is True


def test_already_pinned():

    #message is already pinned

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']


    msg1 = send_msg1(user, channel)

    message.pin({
        'token': user['token'],
        'message_id': msg1['message_id']
    })
    
    with pytest.raises(InputError):
        message.pin({
            'token': user['token'],
            'message_id': msg1['message_id']
        })
        
def test_invalid_id():

    workspace_reset()
    
    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    user2 = reg_user2()
    
    
    with pytest.raises(InputError):
        message.pin({
            'token': user['token'],
            'message_id': 1
        })



def test_unauthor_member():

    #user is not a member of the channel

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()

    msg1 = send_msg1(user, channel1)
    
    with pytest.raises(AccessError):
        message.pin({
            'token': user2['token'],
            'message_id': msg1['message_id'],
        })  


def test_unauth_owner():

    #user is not an owner
    workspace_reset()   
    
    ret = register_and_create()
    user1 = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()

    token = user1['token']
    channel_id = channel1['channel_id']
    u_id = user2['u_id']
    channel.invite(token, channel_id, u_id)

    msg1 = send_msg1(user2, channel1)
    
    with pytest.raises(InputError):
        message.pin({
            'token': user2['token'],
            'message_id': msg1['message_id'],
        })  

