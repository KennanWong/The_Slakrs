'This is the integration test file for channel_messages'
import pytest
import channel
import message
from other import workspace_reset
from test_helper_functions import reg_user2, register_and_create
from error import InputError, AccessError

# pylint: disable=W0612
# pylint: disable=C0103

# pylint compliant

def test_channel_messages_clean():
    'No messages case'
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
    'Invalid channel case'
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
    'Start >= total messages case'
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

    # InputError when start >= total messages, e.g. 50 >= 1
    with pytest.raises(InputError) as e:
        channel.messages(token1, channel_id, 50)

def test_channel_messages_unauthorised():
    'User is not a member case'
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

def test_others1():
    'Other errors, when start is not of type int'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']

    # InputError when start is not an int
    with pytest.raises(InputError) as e:
        channel.messages(token1, channel_id, "asdf")

def test_others2():
    'Other errors, when start is bigger than total number of messages'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']

    # InputError when start is bigger than number of messages
    with pytest.raises(InputError) as e:
        channel.messages(token1, channel_id, 12345)

def test_others3():
    'Other errors, when start is negative'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']

    # InputError when start is negative
    with pytest.raises(InputError) as e:
        channel.messages(token1, channel_id, -1)
