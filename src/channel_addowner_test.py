import pytest
import channel
from other import workspace_reset
from test_helper_functions import reg_user1, reg_user2, register_and_create
from error import InputError, AccessError
from data_stores import get_channel_data_store

def test_channel_add_owner():
    workspace_reset()
    ret = register_and_create()
    user = ret['user']
    token1 = user['token']

    channel1 = ret['channel']
    channel_id = channel1['channel_id']
    
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    # Add user2 as owner
    test = channel.addowner(token1, channel_id, u_id2)

    #owners = channel.details(token2, channel_id)['owner_members']

    channels_store = get_channel_data_store

    assert test in channel1['owners']

def test_already_owner():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']
    
    user2 = reg_user2()
    u_id2 = user1['u_id']

    channel.addowner(token1, channel_id, u_id2)
    
    # InputError because user2 is already an owner
    with pytest.raises(InputError):
        channel.addowner(token1, channel_id, u_id2)

def test_not_owner():
    workspace_reset()
    ret = register_and_create()
    user = ret['user']
    u_id1 = user['u_id']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']
    
    user2 = reg_user2()
    token2 = user2['token']

    # AccessError when non-owner tries to make user1 as owner
    with pytest.raises(AccessError):
        channel.addowner(token2, channel_id, u_id1)