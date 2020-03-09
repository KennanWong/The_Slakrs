import pytest
from error import InputError, AccessError
from auth import auth_register
from channel import channel_leave, channel_details
from channels import channels_create

'''
#############################################################
#                       CHANNEL_LEAVE                       #  
#############################################################

InputError when any of:
** Channel ID is not a valid channel

AccessError when
** Authorised user is not a member of channel with channel_id
'''

def test_channel_leave_successful():
    # CASE 1: Leaving channel
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith') 
    token1 = user1['token']
    u_id1 = user1['u_id']

    user2 = auth_register("john@gmail.com", 'zcvb*&234', 'John', 'Appleseed')
    token2 = user2['token']
    u_id2 = user2['u_id']

    # Create channel
    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    # user2 leaves
    channel_leave(token2, channel_id)

    # Check user2 has left
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

def test_channel_leave_invalid_channel():
    # CASE 2: Leaving an invalid channel
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith') 
    token1 = user1['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    invalidChannelID = 1

    # InputError when user tries to leave an invalid channel
    with pytest.raises(InputError) as e:
        channel_leave(token1, invalidChannelID)

def test_channel_leave_unauthorised():
    # CASE 3: Authorised user is not a member of channel
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith') 
    token1 = user1['token']

    user2 = auth_register("john@gmail.com", 'zcvb*&234', 'John', 'Appleseed')
    token2 = user2['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    
    # AccessError when authorised user is not a member of channel they are 
    # trying to leave from
    # user2 isn't a member
    with pytest.raises(AccessError) as e:
        channel_leave(token2, channel_id)