import pytest
from error import InputError, AccessError
import auth
import channel
import channels
import channel
from other import workspace_reset
from test_helper_functions import reg_user1, register_and_create

#############################################################
#                       CHANNEL_JOIN                        #     
#############################################################

def test_channel_join_successful():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']

    channel.leave(token1, channel_id)  
    channel.join(token1, channel_id) 
    
    assert channel.details(token1, channel_id)['name'] == 'firstChannel'
    assert channel.details(token1, channel_id)['owner_members'] == [{'u_id': u_id1, 'name_first': 'Kennan', 'name_last': 'Wong'}]
    assert channel.details(token1, channel_id)['all_members'] == [{'u_id': u_id1, 'name_first': 'Kennan', 'name_last': 'Wong'}]