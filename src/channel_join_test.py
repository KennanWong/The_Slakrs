
    
import pytest
import channel, channels
from other import workspace_reset
from test_helper_functions import reg_user1, reg_user2, register_and_create
from error import InputError, AccessError

def test_channel_join_successful():
    workspace_reset()
    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']
    channelInfo = ret['channel']
    channel_id = channelInfo['channel_id']

    #channel.leave(token1, channel_id)  
    #channel.join(token1, channel_id) 
    '''
    # Check user2 has joined
    results = [
        {
            "name": 'firstChannel',
            "owner_members": [{
                "u_id": u_id1,
                "name_first": 'Kennan', 
                "name_last": 'Wong'
            }],
            "all_members": [{"
                u_id": 1, 
                "name_first": "Hayden", 
                "name_last": "Smith"}]
        }
    ]
    '''
    assert channel.details(token1, channel_id)['name'] == 'firstChannel'
    assert channel.details(token1, channel_id)['owner_members'] == [{'u_id': u_id1, 'name_first': 'Kennan', 'name_last': 'Wong'}]
    assert channel.details(token1, channel_id)['all_members'] == [{'u_id': u_id1, 'name_first': 'Kennan', 'name_last': 'Wong'}]

def test_channel_join_invalid_channel():
    workspace_reset()
    ret = register_and_create()
    user = ret['user']
    channelInfo = ret['channel']
    
    user2 = reg_user2()
    token = user2['token']
    
    # InputError when user2 tries to join an invalid channel
    # Invalid channel_id = 100
    with pytest.raises(InputError) as e:
        channel.join(token, 100)

def test_channel_join_private():
    workspace_reset()
    user1 = reg_user1()
    payload = {
        'token': user1['token'],
        'name': 'Slackrs',
        'is_public': False
    }
    pvt_channel = channels.create(payload)
    channel_id = pvt_channel['channel_id']
    
    user2 = reg_user2()
    token2 = user2['token']

    # AccessError when user2 tries to join channel where the authorised user 
    # isn't an admin
    with pytest.raises(AccessError) as e:
        channel.join(token2, channel_id)