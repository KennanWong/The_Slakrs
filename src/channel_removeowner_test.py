'This is the integration test file for channel_removeowner'

import pytest
import channel
from other import workspace_reset
from test_helper_functions import reg_user2, register_and_create
from error import InputError, AccessError

# pylint: disable=W0612
# pylint: disable=C0103

# pylint compliant

def test_channel_remove_owner():
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
    channel.addowner(token1, channel_id, u_id2)

    # User2 removes user1 as owner
    channel.removeowner(token2, channel_id, u_id1)

    assert channel.details(token1, channel_id)['owner_members'] == [{
        "u_id": u_id2,
        "name_first": 'Cindy',
        "name_last": 'Tran'
    }]

def test_invalid_channel2():
    'Invalid channel case'
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
    channel.addowner(token1, channel_id, u_id2)

    # Invalid channel_id = 100
    with pytest.raises(InputError) as e:
        channel.removeowner(token2, 100, u_id1)

def test_userid_not_owner():
    'User is not an owner case'
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

    # Invalid user_id = 10
    with pytest.raises(InputError) as e:
        channel.removeowner(token2, channel_id, 100)

def test_not_owner2():
    'Non-owner case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    u_id1 = user1['u_id']
    channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']

    channel_id = channel_info['channel_id']

    with pytest.raises(AccessError) as e:
        channel.removeowner(token2, channel_id, u_id1)
