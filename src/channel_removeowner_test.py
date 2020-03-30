

import pytest
import channel
from other import workspace_reset
from test_helper_functions import reg_user1, reg_user2, register_and_create
from error import InputError, AccessError

def test_channel_remove_owner():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']
    
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel.join(token2, channel_id)
    channel.addowner(token1, channel_id, u_id2)
    channel.removeowner(token2, channel_id, u_id1)

    owners = channel.details(token2, channel_id)['owner_members']

def test_invalid_channel2():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']
    
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']
    
    channel.join(token2, channel_id)
    channel.addowner(token1, channel_id, u_id2)
    
    # Invalid channel_id = 100
    with pytest.raises(InputError):
        channel.removeowner(token2, 100, u_id1)
    
def test_userid_not_owner():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']
    
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']   
    
    channel.join(token2, channel_id)
    channel.addowner(token1, channel_id, u_id2)

    # Invalid user_id = 100
    with pytest.raises(InputError):
        channel.removeowner(token2, channel_id, 100)

def test_not_owner2():
    workspace_reset()
    ret = register_and_create()
    user = ret['user']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']
    
    user2 = reg_user2()
    token = user['token']
    u_id = user['u_id']
    token2 = user2['token'] 
    
    with pytest.raises(AccessError):
        channel.removeowner(token2, channel_id, u_id)
