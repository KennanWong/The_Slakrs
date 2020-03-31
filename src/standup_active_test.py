'this file is the integration tests for standup_active'
from datetime import datetime, timedelta
import pytest

import standup

from other import workspace_reset
from test_helper_functions import register_and_create
from error import InputError


#pylint compliant
#############################################################
#                   STANDUP_ACTIVE                          #
#############################################################
def test_active():
    'testing functionability for standup active'

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
    'testing error case'

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    channel = ret['channel']

    payload = {
        'token': user['token'],
        'channel_id': channel['channel_id'],
        'length': 30
    }

    result = standup.start(payload)                     # pylint: disable=W0612

    payload2 = {
        'token': user['token'],
        'channel_id': 100
    }

    with pytest.raises(InputError):
        standup.start(payload2)                         # pylint: disable=C0304