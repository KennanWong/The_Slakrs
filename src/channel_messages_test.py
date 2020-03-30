import pytest
from error import InputError, AccessError
from auth import auth_register
from channel import channel_messages
from channels import channels_create
from message import message_send

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
	# CASE 1: No messages
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith')
    token1 = user1['token']

    # Create channel
    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    # No message sent to channel
    assert channel_messages(token1, channel_id, 0)["messages"] == []
    assert channel_messages(token1, channel_id, 0)["start"] == 0
    assert channel_messages(token1, channel_id, 0)["end"] == -1

def test_channel_messages_invalid_channel():
	# CASE 2: Messages in an invalid channel
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith')
    token1 = user1['token']
    u_id1 = user1['u_id']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']
    invalidChannelID = 1

    # Send message
    message_send(token1, channel_id, "hello")

	# InputError when we try to check messages in an invalid channel
    with pytest.raises(InputError) as e:
        channel_messages(token1, invalidChannelID, 0)

def test_channel_messages_start_excess():
	# CASE 3: When start > total messages
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith')
    token1 = user1['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    # Send message
    message_send(token1, channel_id, "hello")

	# InputError when start > total messages
    with pytest.raises(InputError) as e:
        channel_messages(token1, channel_id, 50)

def test_channel_messages_unauthorised():
	# CASE 4: Authorised user is not a member of channel with channel_id
    user1 = auth_register("hayden@gmail.com", '123!@asdf', 'Hayden', 'Smith')
    token1 = user1['token']

    user2 = auth_register("john@gmail.com", 'zcvb*&234', 'John', 'Appleseed')
    token2 = user2['token']

    channelInfo = channels_create(token1, 'The Slakrs', True)
    channel_id = channelInfo['channel_id']

    # Send message
    message_send(token1, channel_id, "hello")
    
	# AccessError when user sends message to channel they aren't a member of
    # user2 isn't a member
    with pytest.raises(AccessError) as e:
        channel_messages(token2, channel_id, 0)


import pytest
import channel
import message
from other import workspace_reset
from test_helper_functions import reg_user1, reg_user2, register_and_create
from error import InputError, AccessError

def test_channel_messages_clean():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']

    # No messages in channel
    assert channel.messages(token1, channel_id, 0)["messages"] == []
    assert channel.messages(token1, channel_id, 0)["start"] == 0
    assert channel.messages(token1, channel_id, 0)["end"] == -1

def test_channel_messages_invalid_channel():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']
    
    payload = {
        'token': token1,
        'channel_id': channel_id,
        'message': "hello"
    }

    # Send message
    message.send(payload)

    # InputError when we try to check messages in an invalid channel
    # Invalid channel_id = 100
    with pytest.raises(InputError) as e:
        channel.messages(token1, 100, 0)

def test_channel_messages_start_excess():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']	

    payload = {
        'token': token1,
        'channel_id': channel_id,
        'message': "hello"
    }

    # Send message
    message.send(payload)
    
    # InputError when start > total messages
    with pytest.raises(InputError) as e:
        channel.messages(token1, channel_id, 50)

def test_channel_messages_unauthorised():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']
    user2 = reg_user2()
    token2 = user2['token']
    
    payload = {
        'token': token1,
	    'channel_id': channel_id,
	    'message': "hello"
	}
    
    # Send message
    message.send(payload)

    # AccessError when user sends message to channel they aren't a member of
    # user2 isn't a member
    with pytest.raises(AccessError) as e:
        channel.messages(token2, channel_id, 0)
