'this file is the integration tests for message unpin'

import pytest

import message
import channel
from other import workspace_reset
from test_helper_functions import register_and_create, send_msg1, reg_user2
from error import InputError, AccessError


#pylint compliant
#############################################################
#                   MESSAGE_PIN                             #
#############################################################
def test_unpin():

    'testing functionability for message unpin'

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel1 = ret['channel']

    msg1 = send_msg1(user, channel1)

    message.pin({
        'token': user['token'],
        'message_id': msg1['message_id']
    })

    message.unpin({
        'token': user['token'],
        'message_id': msg1['message_id']
    })

    assert msg1['is_pinned'] is False


def test_already_unpinned():
    'testing error case'
    #message is already unpinned

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel1 = ret['channel']


    msg1 = send_msg1(user, channel1)

    message.pin({
        'token': user['token'],
        'message_id': msg1['message_id']
    })

    message.unpin({
        'token': user['token'],
        'message_id': msg1['message_id']
    })

    with pytest.raises(InputError):
        message.unpin({
            'token': user['token'],
            'message_id': msg1['message_id']
        })

def test_invalid_id():
    'testing error case'
    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    with pytest.raises(InputError):
        message.unpin({
            'token': user['token'],
            'message_id': 1
        })



def test_unauthor_member():
    'testing error case'
    #user is not a member of the channel

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()

    msg1 = send_msg1(user, channel1)

    message.pin({
        'token': user['token'],
        'message_id': msg1['message_id']
    })

    with pytest.raises(AccessError):
        message.unpin({
            'token': user2['token'],
            'message_id': msg1['message_id'],
        })


def test_unauth_owner():
    'testing error case'
    #user is not an owner

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel1 = ret['channel']

    user2 = reg_user2()

    token = user['token']
    channel_id = channel1['channel_id']
    u_id = user2['u_id']
    channel.invite(token, channel_id, u_id)

    msg1 = send_msg1(user, channel1)

    with pytest.raises(InputError):
        message.pin({
            'token': user2['token'],
            'message_id': msg1['message_id'],
        })                                              # pylint: disable=C0304