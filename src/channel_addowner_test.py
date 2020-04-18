'This is the integration test file for channel_addowner'

import pytest
import channel
from other import workspace_reset
from test_helper_functions import reg_user2, reg_user3, register_and_create
from error import InputError, AccessError

# pylint: disable=W0612
# pylint: disable=C0103

# pylint compliant

def test_channel_add_owner():
    'Normal case'
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']
    channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel_id = channel_info['channel_id']

    channel.join(token2, channel_id)

    # Add user2 as owner
    channel.addowner(token1, channel_id, u_id2)

    assert channel.details(token1, channel_id)['owner_members'] == [{
        "u_id": u_id1,
        "name_first": 'Kennan',
        "name_last": 'Wong'
    },
                                                                    {
                                                                        "u_id": u_id2,
                                                                        "name_first": 'Cindy',
                                                                        "name_last": 'Tran'
                                                                    }]

def test_already_owner():
    'Already an owner case'
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel_id = channel_info['channel_id']

    channel.join(token2, channel_id)

    channel.addowner(token1, channel_id, u_id2)

    # InputError because user2 is already an owner
    with pytest.raises(InputError):
        channel.addowner(token1, channel_id, u_id2)

def test_not_owner():
    'Non-owner case'
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']
    user3 = reg_user3()
    token3 = user3['token']
    u_id3 = user3['u_id']

    channel_id = channel_info['channel_id']

    channel.join(token3, channel_id)

    # AccessError when non-owner tries to make user3 as owner
    with pytest.raises(AccessError):
        channel.addowner(token2, channel_id, u_id3)

def test_invalid_channel():
    'Invalid channel case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel_id = channel_info['channel_id']

    channel.join(token2, channel_id)
    channel.addowner(token1, channel_id, u_id2)

    # Invalid channel_id = 100
    with pytest.raises(InputError):
        channel.addowner(token2, 100, u_id2)
