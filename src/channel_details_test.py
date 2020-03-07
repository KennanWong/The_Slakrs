import pytest
from error import InputError, AccessError
from auth import auth_register
from channel import channel_details
from channels import channels_create

'''
#############################################################
#                      CHANNEL_DETAILS                      #      
#############################################################

InputError when any of:
** Channel ID is not a valid channel

AccessError when:
** Authorised user is not a member of channel with channel_id
'''

def test_channel_details():
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']
    u_id1 = user1['u_id']

    # Create channel
    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    
    results = [
        {
            "name": 'The Slakrs',
            "owner_members": [{"u_id": 1, "name_first": "user1", "name_last": "Smith"}],
            "all_members": [{"u_id": 1, "name_first": "user1", "name_last": "Smith"}]
        }
    ]
    assert channel_details(token1, channel_id) == results

def test_channel_details_invalid_channel():
    # Invalid channel
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    invalidChannelID = 1

    with pytest.raises(InputError) as e:
        channel_details(token1, invalidChannelID)

def test_channel_details_unauthorised():
    # Authorised user is not a member of channel with channel_id
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']

    user2 = auth_register("user2@gmail.com", 'zcvb*&234', 'user2', 'Berry')
    token2 = user2['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    with pytest.raises(AccessError) as e:
        channel_details(token2, channel_id)
