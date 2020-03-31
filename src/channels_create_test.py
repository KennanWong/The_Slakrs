'this file is the integration tests for channels create'

import pytest

import channels
from other import workspace_reset
from test_helper_functions import reg_user1
from error import InputError
from data_stores import get_channel_data_store

#pylint compliant

#############################################################
#                   CHANNELS_CREATE                         #
#############################################################
def test_create():

    'testing functionability of channels create'

    workspace_reset()
    user1 = reg_user1()

    payload = {
        'token': user1['token'],
        'name': 'Slackrs',
        'is_public': True

    }

    result1 = channels.create(payload)

    channel_store = get_channel_data_store()

    assert result1 in channel_store


def test_invalid_name():
    'error case for channels create'
    workspace_reset()
    user1 = reg_user1()

    payload = {
        'token': user1['token'],
        'name': 'Thisnameislongerthan20characters',
        'is_public': True
    }


    with pytest.raises(InputError):
        channels.create(payload)
