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
#                   STANDUP_ACTIVE                          #
#############################################################
def test_active():

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

    payload2 = {
        'token': user['token'],
        'channel_id': channel['channel_id']
    }

    result2 = standup.active(payload2)

    length = 30
    time_finish = (datetime.now() + timedelta(seconds=length)).strftime("%H:%M:%S")

    assert result == time_finish
    assert result2['is_active'] is True

def test_invalid_id():
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

    payload2 = {
        'token': user['token'],
        'channel_id': 100
    }

    with pytest.raises(InputError):
        standup.start(payload2)