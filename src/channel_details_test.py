import pytest
import channel
from other import workspace_reset
from test_helper_functions import reg_user1, reg_user2, register_and_create
from error import InputError, AccessError

def test_channel_details_successful():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    u_id1 = user1['u_id']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']

    token1 = user1['token']

    results = [{
            "name": 'The Slakrs',
            "all_members": [{
                "u_id": u_id1,
                "name_first": 'Kennan',
                "name_last": 'Wong'
            }],
            "owner_members": [{
                "u_id": u_id1,
                "name_first": 'Kennan',
                "name_last": 'Wong'
            }]
        }
    ]

    assert channel.details(token1, channel_id) == results

def test_channel_details_invalid_channel():
    workspace_reset()
    ret = register_and_create()
    user = ret['user']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']
	
    token = user['token']

	# InputError when we try to get details of an invalid channel
    # Invalid channel_id = 100
    with pytest.raises(InputError) as e:
        channel.details(token, 100)

def test_channel_details_unauthorised():
	workspace_reset()
	ret = register_and_create()
	user = ret['user']
	channelInfo = ret['channel']
	channel_id = channelInfo['channel_id']
	
	user2 = reg_user2()
	
	token = user2['token']

	# AccessError when we try to get details of channel where the user isn't a 
    # member
    # user2 isn't a member
	with pytest.raises(AccessError) as e:
		channel.details(token, channel_id)