'this file is the integration tests for standup_active'

from datetime import datetime, timedelta
import pytest

import standup

from other import workspace_reset
from test_helper_functions import register_and_create
from error import InputError


#pylint compliant
#############################################################
#                   STANDUP_START                           #
#############################################################
def test_start():
    'testing functionability for standup start'

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
    'testing error case'

    workspace_reset()

    ret = register_and_create()
    user = ret['user']


    payload = {
        'token': user['token'],
        'channel_id': 100,
        'length': 30
    }

    with pytest.raises(InputError):
        standup.start(payload)

def test_already_active():
    'testing error case'

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
        })           # pylint: disable=C0304
    