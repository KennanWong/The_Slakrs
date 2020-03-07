import pytest
from error import InputError, AccessError
from auth import auth_register
from channel import channel_join, channel_details
from channels import channels_create

'''
#############################################################
#                       CHANNEL_JOIN                        #      
#############################################################

InputError when any of:
** Channel ID is not a valid channel

AccessError when
** channel_id refers to a channel that is private (when the authorised user is not an admin)
'''

def test_channel_join_successful():
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith') 
    token1 = user1['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    channel_join(token1, channel_id)

    # Check user has joined
    results = [
        {
            "name": 'The Slakrs',
            "owner_members": [{"u_id": 1, "name_first": "user1", "name_last": "Smith"}],
            "all_members": [{"u_id": 1, "name_first": "user1", "name_last": "Smith"}]
        }
    ]
    assert channel_details(token1, channel_id) == results

def test_channel_join_invalid_channel():
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith') 
    token1 = user1['token']

    user2 = auth_register("user2@gmail.com", 'zcvb*&234', 'user2', 'Berry')
    token2 = user2['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    invalidChannelID = 1

    with pytest.raises(InputError) as e:
        channel_join(token2, invalidChannelID)

def test_channel_join_private():
	# Authorised user is not admin
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith') 
    token1 = user1['token']

    user2 = auth_register("user2@gmail.com", 'zcvb*&234', 'user2', 'Berry')
    token2 = user2['token']

    channelInfo = channels_create(token1, 'The Slakrs', False)
    channel_id = channelInfo['channel_id']
    
    with pytest.raises(AccessError) as e:
        channel_join(token2, channel_id)