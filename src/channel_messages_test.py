import pytest
from error import InputError, AccessError
from auth import auth_register
from channel import channel_messages
from channels import channels_create

'''
#############################################################
#                     CHANNEL_MESSAGES                      #      
#############################################################

InputError when any of:
** Channel ID is not a valid channel
** start is greater than the total number of messages in the channel

AccessError when
** Authorised user is not a member of channel with channel_id
'''

def test_channel_messages_clean():
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    assert channel_messages(token1, channel_id, 0)["messages"] == []
    assert channel_messages(token1, channel_id, 0)["start"] == 0
    assert channel_messages(token1, channel_id, 0)["end"] == -1

def test_channel_messages_invalid_channel():
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']
    u_id1 = user1['u_id']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    invalidChannelID = 1

    with pytest.raises(InputError) as e:
        channel_messages(token1, invalidChannelID, 0)

def test_channel_messages_start_plus():
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    with pytest.raises(InputError) as e:
        channel_messages(token1, channel_id, 50)

def test_channel_messages_unauthorised():
    user1 = auth_register("user1@gmail.com", '123!@asdf', 'user1', 'Smith')
    token1 = user1['token']

    user2 = auth_register("user2@gmail.com", 'zcvb*&234', 'user2', 'Berry')
    token2 = user2['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    with pytest.raises(AccesssError) as e:
        channel_messages(token2, channel_id, 0)
