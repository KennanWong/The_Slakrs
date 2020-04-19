'This is the integration test file for admin_user_remove'

import pytest
import channel
from admin_user_remove import user_remove
from other import workspace_reset
from test_helper_functions import reg_user1, reg_user2, register_and_create, send_msg1
from helper_functions import check_owner_slackr, user_details
from data_stores import get_channel_data_store, get_messages_store
from error import InputError, AccessError

# pylint: disable=W0612
# pylint: disable=C0103

# pylint compliant

def test_admin_user_remove_successful1():
    'Successful case with registering'
    workspace_reset()

    user1 = reg_user1()
    token1 = user1['token']
    u_id1 = user1['u_id']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    payload = {
        'token': token1,
        'u_id': u_id2
    }
    # Remove user1 from slackr
    user_remove(payload)

def test_admin_user_remove_successful2():
    'Successful case with channels'
    workspace_reset()
    channel_store = get_channel_data_store()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel_info = ret['channel']
    channel_id = channel_info['channel_id']

    channel.join(token2, channel_id)

    payload = {
        'token': token1,
        'u_id': u_id2
    }

    # Remove user2 from slackr
    user_remove(payload)

    user2_dets = user_details(u_id2)
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

def test_admin_user_remove_successful3():
    'Successful case with messages'
    workspace_reset()
    channel_store = get_channel_data_store()
    messages_store = get_messages_store()

    ret = register_and_create()
    user1 = ret['user']
    token1 = user1['token']
    u_id1 = user1['u_id']
    user2 = reg_user2()
    token2 = user2['token']
    u_id2 = user2['u_id']

    channel_info = ret['channel']
    channel_id = channel_info['channel_id']

    channel.join(token2, channel_id)

    payload = {
        'token': token1,
        'u_id': u_id2
    }

    msg1 = send_msg1(user2, channel_info)

    # Remove user1 from slackr
    user_remove(payload)

    user2_dets = user_details(u_id2)
    channel_info = ret['channel']
    channel_id = channel_info['channel_id']
    for curr_channel in channel_store:
        channel_id = curr_channel['channel_id']
        if user2_dets in curr_channel['members']:
            assert channel.details(token1, channel_id)['all_members'] == [{
                "u_id": u_id1,
                "name_first": 'Kennan',
                "name_last": 'Wong'
            }]
        if user2_dets in curr_channel['owners']:
            assert channel.details(token1, channel_id)['owner_members'] == [{
                "u_id": u_id1,
                "name_first": 'Kennan',
                "name_last": 'Wong'
            }]

    assert msg1 not in messages_store
    assert msg1 not in channel_info['messages']

    #for messages in message_store:
        #if message_belong_user(token2, messageS['message_id])




def test_invalid_userid():
    'Invalid user case'
    workspace_reset()

    user1 = reg_user1()
    token1 = user1['token']

    # Invalid user_id = 100
    payload = {
        'token': token1,
        'u_id': 100
    }
    # InputError when trying to remove user from slackr with invalid user ID
    with pytest.raises(InputError) as e:
        user_remove(payload)

def test_unauthorised_slackr():
    'Authorised user is not an owner of slackr case'
    workspace_reset()

    user1 = reg_user1()
    u_id1 = user1['u_id']
    user2 = reg_user2()
    token2 = user2['token']

    payload = {
        'token': token2,
        'u_id': u_id1
    }
    if not check_owner_slackr(token2):
        # AccessError when authorised user isn't an owner and tries to remove someone from the
        # slackr
        with pytest.raises(AccessError) as e:
            user_remove(payload)
