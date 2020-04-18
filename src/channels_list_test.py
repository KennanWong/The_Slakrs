'this file is the integration tests for channels list'

import pytest           #pylint disable = W0611

import channels
from other import workspace_reset
from test_helper_functions import  register_and_create, reg_user2


#pylint compliant

#############################################################
#                   CHANNELS_LIST                           #
#############################################################
def test_list():

    'testing functionability of channels list'

    workspace_reset()

    ret = register_and_create()
    user = ret['user']
    token = user['token']

    result1 = channels.List(token)

    expected = {
        'channel_id' : 1,
        'name': 'firstChannel'
    }

    assert expected in result1


def test_list2():
    'testing alternate case of channels list'
    workspace_reset()

    ret = register_and_create()

    user2 = reg_user2()
    token2 = user2['token']

    payload1 = {
        'token': token2,
        'name': 'Slackrs',
        'is_public': True
    }
    result1 = channels.create(payload1)

    result2 = channels.List(token2)

    expected = {
        'channel_id': 2,
        'name': 'Slackrs'
    }

    assert expected in result2      #pylint disable = C0305
