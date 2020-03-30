import pytest

import standup
#import channel
import channels
from other import workspace_reset
from test_helper_functions import reg_user1, register_and_create, send_msg1, reg_user2
from error import InputError, AccessError
from data_stores import get_channel_data_store, get_messages_store
import time
from datetime import datetime, timedelta
from helper_functions import addSecs

#############################################################
#                   STANDUP_START                           #
#############################################################
def test_start():

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    payload = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 30
    }

    result = standup.start(payload)
    length = 30
    time_finish = (datetime.now() + timedelta(seconds=length)).strftime("%H:%M:%S")
    assert result == time_finish

def test_invalid_id():

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    payload = {
        'token': user['token'],
        'channel_id': 100,
        'length': 30
    }

    with pytest.raises(InputError):
        standup.start(payload)

def test_already_active():

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    standup.start({
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 30
    })

    with pytest.raises(InputError):
        standup.start({
            'token': user['token'],
            'channel_id': channel['channel_id'],
            'length': 35
        })

    