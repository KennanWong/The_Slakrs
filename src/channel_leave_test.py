
import pytest
import channel
from other import workspace_reset
from test_helper_functions import reg_user1, reg_user2, register_and_create
from error import InputError, AccessError

def test_channel_leave_successful():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    u_id1 = user1['u_id']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']

    #user2 = reg_user2()
    #token2 = user2['token']

    #channel.join(token2, channel_id)
    #channel.leave(token2, channel_id)
    '''
    # Check user2 has left
    results = [{
            "name": 'The Slakrs',
            "owner_members": [{
                "u_id": u_id1,
                "name_first": 'Kennan',
                "name_last": 'Wong'
            }],
            "all_members": [{
                "u_id": u_id1,
                "name_first": 'Kennan',
                "name_last": 'Wong'
            }]
        }
    ]
    s
    assert channel.details(token1, channel_id) == results
    '''
    assert channel.details(token1, channel_id)['name'] == 'firstChannel'
    assert channel.details(token1, channel_id)['owner_members'] == [{'u_id': u_id1, 'name_first': 'Kennan', 'name_last': 'Wong'}]
    assert channel.details(token1, channel_id)['all_members'] == [{'u_id': u_id1, 'name_first': 'Kennan', 'name_last': 'Wong'}]

def test_channel_leave_invalid_channel():
    workspace_reset()
    ret = register_and_create()
    user = ret['user']
    channelInfo = ret['channel']

    token = user['token']

    # InputError when user tries to leave an invalid channel
    # Invalid channel_id = 100
    with pytest.raises(InputError) as e:
        channel.leave(token, 100)

def test_channel_leave_unauthorised():
    workspace_reset()
    ret = register_and_create()
    user = ret['user']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']

    user2 = reg_user2()

    token1 = user['token']
    token2 = user2['token']

    # AccessError when authorised user is not a member of channel they are 
    # trying to leave from
    # user2 isn't a member
    with pytest.raises(AccessError) as e:
        channel.leave(token2, channel_id)
        