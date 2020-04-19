'This is the integration test file for channel_join'

import pytest
import channel
import channels
from other import workspace_reset
from test_helper_functions import reg_user1, reg_user2, register_and_create
from error import InputError, AccessError

# pylint: disable=W0612
# pylint: disable=C0103

# pylint compliant

def test_channel_join_successful():
    'Successful case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']
    channel_info = ret['channel']
    channel_id = channel_info['channel_id']

    channel.leave(token1, channel_id)
    channel.join(token1, channel_id)

    assert channel.details(token1, channel_id)['name'] == 'firstChannel'
    assert channel.details(token1, channel_id)['owner_members'] == [{
        'u_id': u_id1,
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }]
    assert channel.details(token1, channel_id)['all_members'] == [{
        'u_id': u_id1,
        'name_first': 'Kennan',
        'name_last': 'Wong'
    }]

def test_channel_join_invalid_channel():
    'Invalid channel case'
    workspace_reset()

    ret = register_and_create()
    channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']

    # InputError when user2 tries to join an invalid channel
    # Invalid channel_id = 100
    with pytest.raises(InputError) as e:
        channel.join(token2, 100)

def test_channel_join_private():
    'Private channel case'
    workspace_reset()

    user1 = reg_user1()
    payload = {
        'token': user1['token'],
        'name': 'Slackrs',
        'is_public': False
    }
    pvt_channel = channels.create(payload)
    channel_id = pvt_channel['channel_id']

    user2 = reg_user2()
    token2 = user2['token']

    # AccessError when user2 tries to join channel where the authorised user
    # isn't an admin
    with pytest.raises(AccessError) as e:
        channel.join(token2, channel_id)
