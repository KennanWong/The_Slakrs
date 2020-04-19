'This is the integration test file for channel_leave'

import pytest
import channel
from other import workspace_reset
from test_helper_functions import reg_user2, register_and_create
from error import InputError, AccessError

#pylint: disable=W0612
#pylint: disable=C0103

#pylint compliant

def test_channel_leave_successful():
    'Sucessful case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']
    channel_info = ret['channel']
    channel_id = channel_info['channel_id']

    user2 = reg_user2()
    token2 = user2['token']

    channel.join(token2, channel_id)
    channel.leave(token2, channel_id)

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

def test_channel_leave_invalid_channel():
    'Invalid channel case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channel_info = ret['channel']

    # InputError when user tries to leave an invalid channel
    # Invalid channel_id = 100
    with pytest.raises(InputError) as e:
        channel.leave(token1, 100)

def test_channel_leave_unauthorised():
    'User is not a member'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']

    channel_id = channel_info['channel_id']

    # AccessError when authorised user is not a member of channel they are
    # trying to leave from
    # user2 isn't a member
    with pytest.raises(AccessError) as e:
        channel.leave(token2, channel_id)
        