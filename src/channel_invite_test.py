'This is the integration test file for channel_invite'

import pytest
import channel
from other import workspace_reset
from test_helper_functions import reg_user2, reg_user3, register_and_create
from error import InputError, AccessError

# pylint: disable=W0612
# pylint: disable=C0103

# pylint compliant

def test_channel_invite_successful():
    'Successful case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channel_info = ret['channel']
    user2 = reg_user2()
    u_id2 = user2['u_id']

    channel_id = channel_info['channel_id']

    assert channel.invite(token1, channel_id, u_id2) == {}

def test_channel_invite_invalid_channel():
    'Invalid channel case'
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channel_info = ret['channel']
    user2 = reg_user2()
    u_id2 = user2['u_id']

	# InputError when user2 is invited to an invalid channel
    # Invalid channel_id = 100
    with pytest.raises(InputError) as e:
        channel.invite(token1, 100, u_id2)

def test_channel_invite_invalid_userid():
    'Invalid user case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token = user1['token']
    channel_info = ret['channel']
    channel_id = channel_info['channel_id']

    # InputError when user tries to invite someone with an invalid user ID
    # Invalid user_id = 100
    with pytest.raises(InputError) as e:
        channel.invite(token, channel_id, 100)

def test_channel_invite_unauthorised():
    'User is not a member case'
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']
    user3 = reg_user3()
    u_id3 = user3['u_id']

    channel_id = channel_info['channel_id']

    # AccessError when authorised user is not a member of the channel
    # user2 invites user3 after user1 creates the channel
    with pytest.raises(AccessError) as e:
        channel.invite(token2, channel_id, u_id3)

def test_channel_invite_existing_user():
    'Existing user case'
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channel_info = ret['channel']
    user2 = reg_user2()
    u_id2 = user2['u_id']

    channel_id = channel_info['channel_id']

    # Invite user2
    channel.invite(token1, channel_id, u_id2)

    # InputError when user tries to invite someone who is already a member of
    # the channel
    with pytest.raises(InputError) as e:
        channel.invite(token1, channel_id, u_id2)
