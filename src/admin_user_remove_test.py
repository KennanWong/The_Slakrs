'This is the integration test file for admin_user_remove'

import pytest
import channel
from admin_user_remove import user_remove
from other import workspace_reset
from test_helper_functions import reg_user1, reg_user2, register_and_create
from error import InputError, AccessError
from helper_functions import check_owner_slackr, user_details
from data_stores import get_channel_data_store, get_messages_store

def test_admin_user_remove_successful():
    'Successful case'
    workspace_reset()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    #user1 = reg_user1()
    u_id1 = user1['u_id']
    #token1 = user1['token']
    #channel_info = ret['channel']
    user2 = reg_user2()
    #token2 = user2['token']
    u_id2 = user2['u_id']

    #channel_id = channel_info['channel_id']

    #channel.join(token2, channel_id)
    # User2 is owner
    #channel.addowner(token1, channel_id, u_id2)
    channel_store = get_channel_data_store()
    payload = {
        'token': token1,
        'u_id': u_id2
    }
    # Remove user1 from slackr
    user_remove(payload)

    user2_dets = user_details(u_id2)
    channel_info = ret['channel']
    channel_id = channel_info['channel_id']
    for channel_lol in channel_store:
        channel_id = channel_lol['channel_id']
        if user2_dets in channel_lol['members']:
            assert channel.details(token1, channel_id)['all_members'] == [{
                "u_id": u_id1,
                "name_first": 'Kennan',
                "name_last": 'Wong'
            }]
        if user2_dets in channel_lol['owners']:
            assert channel.details(token1, channel_id)['owner_members'] == [{
                "u_id": u_id1,
                "name_first": 'Kennan',
                "name_last": 'Wong'
            }]

    #messages_store = get_messages_store()
    #if  

def test_invalid_userid():
    'Invalid user case'
    workspace_reset()

    #ret = register_and_create()
    #user1 = ret['user']
    #token1 = user1['token']
    #channel_info = ret['channel']
    user2 = reg_user2()
    token2 = user2['token']
    #u_id2 = user2['u_id']

    #channel_id = channel_info['channel_id']

    #channel.join(token2, channel_id)
    # User2 is owner
    #channel.addowner(token1, channel_id, u_id2)

    payload = {
        'token': token2,
        'u_id': 100
    }
    # InputError when trying to remove user from slackr with invalid user ID
    # Invalid user_id = 100
    with pytest.raises(InputError) as e:
        user_remove(payload)

def test_unauthorised_slackr():
    'Authorised user is not an owner of slackr case'
    workspace_reset()

    #ret = register_and_create()
    #user1 = ret['user']
    #channel_info = ret['channel']
    user1 = reg_user1()
    #token1 = user1['token']
    u_id1 = user1['u_id']
    user2 = reg_user2()
    token2 = user2['token']
    #u_id2 = user2['u_id']

    #channel_id = channel_info['channel_id']

    #channel.join(token3, channel_id)
    payload = {
        'token': token2,
        'u_id': u_id1
    }
    if not check_owner_slackr(token2):
        # AccessError when authorised user isn't an owner and tries to remove someone from the slackr
        # User2 tries to remove user3               after user1 creates the channel
        with pytest.raises(AccessError) as e:
            user_remove(payload)
'''
def test_remove_from_channels():
    channel_store = get_channel_data_store()
    ret = register_and_create()
    token1 = ret['token']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']
    user2_dets = user_details(u_id2)
    channel_info = ret['channel']
    channel_id = channel_info['channel_id']
    channel.join(token2, channel_id)
    for channelx in channel_store:
        if user2_dets in channelx['members']:
            payload = {
                'token': token1,
                'u_id': u_id2
            }
            user_remove(payload)
'''