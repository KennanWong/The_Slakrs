'This is the integration test file for channel_details'

import pytest
import channel
from other import workspace_reset
from test_helper_functions import reg_user2, register_and_create
from error import InputError, AccessError

# pylint: disable=W0612
# pylint: disable=C0103

# pylint compliant

def test_channel_details_successful():
    'Successful case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']

    channel_info = ret['channel']
    channel_id = channel_info['channel_id']

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

def test_channel_details_invalid_channel():
    'Invalid channel case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channel_info = ret['channel']

	# InputError when we try to get details of an invalid channel
    # Invalid channel_id = 100
    with pytest.raises(InputError) as e:
        channel.details(token1, 100)

def test_channel_details_unauthorised():
    'User is not a member case'
    workspace_reset()

    ret = register_and_create()
    channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']

    channel_id = channel_info['channel_id']

	# AccessError when we try to get details of channel where the user isn't a
    # member
    # user2 isn't a member
    with pytest.raises(AccessError) as e:
        channel.details(token2, channel_id)
