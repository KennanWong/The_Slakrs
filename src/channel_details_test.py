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

def test_channel_details_successful():
    # CASE 1: Matching details to expected output
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith')
    token1 = user1['token']
    u_id1 = user1['u_id']

    # Create channel
    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    
    results = [
        {
            "name": 'The Slakrs',
            "owner_members": [{"u_id": 1, "name_first": "Hayden", 
                               "name_last": "Smith"}],
            "all_members": [{"u_id": 1, "name_first": "Hayden", 
                             "name_last": "Smith"}]
        }
    ]

    assert channel_details(token1, channel_id) == results

def test_channel_details_invalid_channel():
    # CASE 2: Invalid channel
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith')
    token1 = user1['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    invalidChannelID = 1

    # InputError when we try to get details of an invalid channel
    with pytest.raises(InputError) as e:
        channel_details(token1, invalidChannelID)

def test_channel_details_unauthorised():
    # CASE 3: Authorised user is not a member of channel with channel_id
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith')
    token1 = user1['token']

    user2 = auth_register("john@gmail.com", 'zcvb*&234', 'John', 'Appleseed')
    token2 = user2['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    # AccessError when we try to get details of channel where the user isn't a 
    # member
    # user2 isn't a member
    with pytest.raises(AccessError) as e:
        channel_details(token2, channel_id)